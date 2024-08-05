package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus.LIVE;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.ChangeCampaignTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.RemoveCampaignTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineCampaignDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineCampaignRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.context.annotation.Lazy;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class TimelineCampaignService extends AbstractService<Campaign> {

  private final TimelineCampaignRepository customRepository;
  private final TimelinePostService timelinePostService;
  private final TimelineKafkaPublisher timelineKafkaPublisher;

  public TimelineCampaignService(
      TimelineCampaignRepository repository,
      @Lazy TimelinePostService timelinePostService,
      TimelineKafkaPublisher timelineKafkaPublisher) {
    super(repository);
    this.customRepository = repository;
    this.timelinePostService = timelinePostService;
    this.timelineKafkaPublisher = timelineKafkaPublisher;
  }

  @Override
  @SuppressWarnings("unchecked")
  public Campaign save(Campaign entity) {
    validate(entity);

    Campaign savedCampaign = super.save(entity);

    if (savedCampaign.isScheduled()) {
      sendCreateMessage(savedCampaign);
    }
    return savedCampaign;
  }

  @Override
  public Campaign update(Campaign existingEntity, Campaign updateEntity) {
    validate(updateEntity);

    Campaign savedCampaign = repository.save(updateEntity);

    if (isAboutToClose(existingEntity, updateEntity)) {
      sendDeleteMessage(updateEntity);
      timelinePostService.unpublishByCampaignId(savedCampaign.getId());
    } else if (existingEntity.isScheduled()) {
      sendUpdateMessage(savedCampaign);
    } else if (updateEntity.isScheduled()) {
      sendCreateMessage(savedCampaign);
    }

    return savedCampaign;
  }

  @Override
  public void delete(String id) {
    Campaign campaignToDelete = repository.findById(id).orElseThrow(NotFoundException::new);

    super.delete(id);

    if (campaignToDelete.getPostsIds() != null) {
      for (String postId : campaignToDelete.getPostsIds()) {
        this.timelinePostService.delete(postId);
      }
    }
    if (campaignToDelete.getStatus() == LIVE) {
      sendDeleteMessage(campaignToDelete);
    }
  }

  public List<Campaign> findOrdered(Sort sort) {
    return repository.findAll(sort);
  }

  public List<Campaign> findByBrandOrdered(String brand, Sort sort) {
    return repository.findByBrand(brand, sort);
  }

  public Optional<Campaign> findCurrentLiveCampaignByBrand(String brand) {
    return customRepository.findCurrentLiveCampaignByBrand(brand, Instant.now());
  }

  private void validate(Campaign entity) {
    if (entity.getStatus() == LIVE) {
      customRepository
          .findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(
              entity.getId(), entity.getBrand(), LIVE, Instant.now())
          .ifPresent(
              (Campaign campaign) -> {
                throw new ValidationException(
                    String.format(
                        "Cannot save the Campaign since the existing '%s' Campaign might be displayed to "
                            + "the customers. You have to close it first",
                        campaign.getName()));
              });
    }
  }

  private boolean isAboutToClose(Campaign existingEntity, Campaign updateEntity) {
    return existingEntity.isScheduled() && updateEntity.isExpired();
  }

  private void sendCreateMessage(Campaign savedCampaign) {
    TimelineMessageDto campaignPostMessage =
        new TimelineCampaignDto()
            .setDisplayFrom(savedCampaign.getDisplayFrom())
            .setDisplayTo(savedCampaign.getDisplayTo())
            .setPageSize(savedCampaign.getMessagesToDisplayCount())
            .setId(savedCampaign.getId())
            .setCreatedDate(savedCampaign.getCreatedAt())
            .setBrand(savedCampaign.getBrand());
    sendCampaignMessage(campaignPostMessage);
  }

  private void sendUpdateMessage(Campaign savedCampaign) {
    TimelineMessageDto changeCampaignMessage =
        new ChangeCampaignTimelineMessageDto()
            .setData(
                (TimelineCampaignDto)
                    new TimelineCampaignDto()
                        .setDisplayFrom(savedCampaign.getDisplayFrom())
                        .setDisplayTo(savedCampaign.getDisplayTo())
                        .setPageSize(savedCampaign.getMessagesToDisplayCount())
                        .setId(savedCampaign.getId())
                        .setCreatedDate(savedCampaign.getCreatedAt())
                        .setBrand(savedCampaign.getBrand()))
            .setAffectedMessageId(savedCampaign.getId())
            .setAffectedMessageCreatedDate(savedCampaign.getCreatedAt())
            .setId(UUID.randomUUID().toString())
            .setCreatedDate(Instant.now())
            .setBrand(savedCampaign.getBrand());

    sendCampaignMessage(changeCampaignMessage);
  }

  private void sendDeleteMessage(Campaign campaignToDelete) {
    TimelineMessageDto deleteCampaignMessage =
        new RemoveCampaignTimelineMessageDto()
            .setAffectedMessageId(campaignToDelete.getId())
            .setAffectedMessageCreatedDate(campaignToDelete.getCreatedAt())
            .setCreatedDate(Instant.now())
            .setId(UUID.randomUUID().toString())
            .setBrand(campaignToDelete.getBrand());
    sendCampaignMessage(deleteCampaignMessage);
  }

  private void sendCampaignMessage(TimelineMessageDto campaignMessage) {
    this.timelineKafkaPublisher.publishTimelineMessage(campaignMessage.getBrand(), campaignMessage);
  }
}
