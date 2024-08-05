package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.ChangePostTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.RemovePostTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelinePostDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.PostStatus;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelinePost;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.mapping.TemplateMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.time.Instant;
import java.util.Collection;
import java.util.List;
import java.util.UUID;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class TimelinePostService extends AbstractService<TimelinePost> {

  private final TimelinePostPageRepository postRepository;
  private final TimelineCampaignService campaignService;
  private final TimelineKafkaPublisher timelineKafkaPublisher;

  public TimelinePostService(
      TimelinePostPageRepository repository,
      TimelineCampaignService campaignService,
      TimelineKafkaPublisher timelineKafkaPublisher) {
    super(repository);
    this.postRepository = repository;
    this.campaignService = campaignService;
    this.timelineKafkaPublisher = timelineKafkaPublisher;
  }

  public List<TimelinePost> findPageByBrandAndCampaignId(
      String brand, String campaignId, Pageable pageable) {
    return postRepository.findPageByBrandAndCampaignId(brand, campaignId, pageable);
  }

  public List<TimelinePost> findByBrandAndCampaignId(String brand, String campaignId, Sort sort) {
    return postRepository.findByBrandAndCampaignId(brand, campaignId, sort);
  }

  public int getCountByBrandAndCampaignId(String brand, String campaignId) {
    return postRepository.countByBrandAndCampaignId(brand, campaignId);
  }

  @Override
  @SuppressWarnings("unchecked")
  public TimelinePost save(TimelinePost entity) {
    verify(entity);

    TimelinePost savedPost = postRepository.save(entity);

    if (isAlreadyPublished(savedPost)) {
      sendPostMessage(savedPost);
    }
    return savedPost;
  }

  @Override
  public void delete(String id) {
    TimelinePost postToDelete = postRepository.findById(id).orElseThrow(NotFoundException::new);

    super.delete(id);
    sendRemovePostMessage(postToDelete);
  }

  @Override
  public TimelinePost update(TimelinePost existingEntity, TimelinePost updateEntity) {
    verify(updateEntity);

    boolean postIsAboutToPublish = isAboutToPublish(existingEntity, updateEntity);
    if (postIsAboutToPublish) {
      updateEntity.setPublishedAt(Instant.now());
    }

    TimelinePost updatedPost = postRepository.save(updateEntity);

    if (postIsAboutToPublish) {
      sendPostMessage(updatedPost);
    } else if (isAboutToUnpublish(existingEntity, updatedPost)) {
      sendRemovePostMessage(updatedPost);
    } else if (isAlreadyPublished(existingEntity)) {
      sendChangePostMessage(updatedPost);
    }

    return updatedPost;
  }

  public void unpublishByCampaignId(String campaignId) {
    Collection<TimelinePost> posts = postRepository.findByCampaignId(campaignId);

    posts.forEach(TimelinePost::unpublish);

    postRepository.saveAll(posts);
  }

  public void republishByCampaignId(String campaignId) {
    postRepository
        .findByCampaignIdAndPostStatusIs(campaignId, PostStatus.PUBLISHED)
        .forEach(this::sendPostMessage);
  }

  private void verify(TimelinePost entity) {
    if (entity.getPostStatus() != PostStatus.DRAFT) {
      Campaign campaign =
          campaignService
              .findOne(entity.getCampaignId())
              .orElseThrow(() -> new NotFoundException("No associated Campaign found"));

      if (!campaign.isDisplayed()) {
        throw new ValidationException(
            "You can only operate DRAFT posts while Campaign is not displayed to the customers");
      }
    }
  }

  private void sendPostMessage(TimelinePost savedPost) {
    TimelineMessageDto post =
        new TimelinePostDto()
            .setCampaignId(savedPost.getCampaignId())
            .setCampaignName(savedPost.getCampaignName())
            .setPinned(savedPost.isPinned())
            .setTemplate(TemplateMapper.INSTANCE.toDto(savedPost.getTemplate()))
            .setId(savedPost.getId())
            .setCreatedDate(savedPost.getPublishedAt())
            .setBrand(savedPost.getBrand());

    sendTimelinePostMessage(post);
  }

  private void sendChangePostMessage(TimelinePost updatedPost) {
    TimelineMessageDto changePostMessage =
        new ChangePostTimelineMessageDto()
            .setData(
                (TimelinePostDto)
                    new TimelinePostDto()
                        .setCampaignId(updatedPost.getCampaignId())
                        .setCampaignName(updatedPost.getCampaignName())
                        .setPinned(updatedPost.isPinned())
                        .setTemplate(TemplateMapper.INSTANCE.toDto(updatedPost.getTemplate()))
                        .setId(updatedPost.getId())
                        .setCreatedDate(updatedPost.getPublishedAt())
                        .setBrand(updatedPost.getBrand()))
            .setAffectedMessageId(updatedPost.getId())
            .setAffectedMessageCreatedDate(updatedPost.getPublishedAt())
            .setId(UUID.randomUUID().toString())
            .setCreatedDate(Instant.now())
            .setBrand(updatedPost.getBrand());

    sendTimelinePostMessage(changePostMessage);
  }

  private void sendRemovePostMessage(TimelinePost postToDelete) {
    TimelineMessageDto removePostMessage =
        new RemovePostTimelineMessageDto()
            .setAffectedMessageId(postToDelete.getId())
            .setAffectedMessageCreatedDate(postToDelete.getPublishedAt())
            .setCreatedDate(Instant.now())
            .setId(UUID.randomUUID().toString())
            .setBrand(postToDelete.getBrand());

    sendTimelinePostMessage(removePostMessage);
  }

  private boolean isAlreadyPublished(TimelinePost existingEntity) {
    return existingEntity.getPostStatus() == PostStatus.PUBLISHED;
  }

  private boolean isAboutToPublish(TimelinePost existingEntity, TimelinePost updatedPost) {
    return existingEntity.getPostStatus() != PostStatus.PUBLISHED
        && isAlreadyPublished(updatedPost);
  }

  private boolean isAboutToUnpublish(TimelinePost existingEntity, TimelinePost updatedPost) {
    return existingEntity.getPostStatus() != PostStatus.UNPUBLISHED
        && updatedPost.getPostStatus() == PostStatus.UNPUBLISHED;
  }

  private void sendTimelinePostMessage(TimelineMessageDto messageDto) {
    this.timelineKafkaPublisher.publishTimelineMessage(messageDto.getBrand(), messageDto);
  }
}
