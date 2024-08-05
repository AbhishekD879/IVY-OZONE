package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.CustomPageImpl;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.PostMessageService;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class PostMessageServiceImpl implements PostMessageService {
  private final PostRepository postRepository;
  private final CampaignRepository campaignRepository;

  @Override
  public Page<PostMessage> findPage(int page) {
    return findActive()
        .map(
            (CampaignMessage campaign) -> {
              List<PostMessage> postMessages = new ArrayList<>();
              Iterable<PostMessage> postMessageIterator =
                  postRepository.findByCampaignId(campaign.getId());
              postMessageIterator.forEach(postMessages::add);
              int count = postMessages.size();
              postMessages.sort(PostRepository.POST_COMPARATOR);
              int fromIndex = page * campaign.getPageSize();
              int toIndex = fromIndex + campaign.getPageSize();
              toIndex = toIndex > postMessages.size() ? postMessages.size() : toIndex;
              postMessages = postMessages.subList(fromIndex, toIndex);
              return new CustomPageImpl<>(
                  postMessages, PageRequest.of(page, campaign.getPageSize()), count);
            })
        .orElse(new CustomPageImpl<>(Collections.emptyList()));
  }

  @SuppressWarnings("squid:S2293")
  @Override
  public Page<PostMessage> findPageBefore(Message.TimeBasedId id) {
    return findActive()
        .map(
            (CampaignMessage campaignMessage) -> {
              List<PostMessage> postMessages = new ArrayList<>();
              Iterable<PostMessage> postMessageIterator =
                  postRepository.findByCampaignId(campaignMessage.getId());
              postMessageIterator.forEach(postMessages::add);
              postMessages.sort(PostRepository.POST_COMPARATOR);
              int fromIndex = 0;
              for (PostMessage postMessage : postMessages) {
                if (postMessage.getId().equals(id.getId())) {
                  break;
                }
                fromIndex++;
              }
              fromIndex++;
              int sizeOfPostMessages = postMessages.size();
              int toIndex = fromIndex + campaignMessage.getPageSize();
              toIndex = toIndex > sizeOfPostMessages ? sizeOfPostMessages : toIndex;
              if (fromIndex < toIndex) {
                return new CustomPageImpl<>(
                    postMessages.subList(fromIndex, toIndex),
                    PageRequest.of(
                        fromIndex / campaignMessage.getPageSize(), campaignMessage.getPageSize()),
                    sizeOfPostMessages);
              }
              return new CustomPageImpl<PostMessage>(Collections.emptyList());
            })
        .orElse(new CustomPageImpl<>(Collections.emptyList()));
  }

  private Optional<CampaignMessage> findActive() {
    List<CampaignMessage> campaignMessages = new ArrayList<>();
    Iterable<CampaignMessage> postMessageIterator = campaignRepository.findAll();
    postMessageIterator.forEach(campaignMessages::add);
    return campaignMessages.stream().filter(this::isWithinTimeframe).findAny();
  }

  private boolean isWithinTimeframe(CampaignMessage campaignMessage) {
    return campaignMessage.getDisplayFrom().isBefore(Instant.now())
        && campaignMessage.getDisplayTo().isAfter(Instant.now());
  }
}
