package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.controller.event.SocketEvent;
import com.ladbrokescoral.oxygen.timeline.api.handlers.ReactiveWsMessageHandler;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.in.LoadPostPageFromInputMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.PostMessageDto;
import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.reactive.model.MessageContent;
import com.ladbrokescoral.oxygen.timeline.api.repository.CustomPageImpl;
import java.util.Collection;
import java.util.Collections;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.modelmapper.TypeToken;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class LoadNextPageMessageService {
  private final PostMessageService postMessageService;
  private final ModelMapper modelMapper;

  public void onLoadPageEvent(
      ReactiveWsMessageHandler handler, LoadPostPageFromInputMessage loadPageMessage) {
    Page<PostMessage> page =
        postMessageService.findPageBefore(
            new Message.TimeBasedId(
                loadPageMessage.getFrom().getId(), loadPageMessage.getFrom().getTimestamp()));
    if (page.getTotalElements() == 0) {
      handler.handleMessage(
          MessageContent.withPayload(
              SocketEvent.POST_PAGE.name(), new CustomPageImpl<>(Collections.emptyList())));
    } else {
      handler.handleMessage(
          MessageContent.withPayload(
              SocketEvent.POST_PAGE.name(),
              new CustomPageImpl<>(
                  modelMapper.map(
                      page.getContent(), new TypeToken<Collection<PostMessageDto>>() {}.getType()),
                  PageRequest.of(
                      page.getPageable().getPageNumber(), page.getPageable().getPageSize()),
                  page.getTotalElements())));
    }
  }
}
