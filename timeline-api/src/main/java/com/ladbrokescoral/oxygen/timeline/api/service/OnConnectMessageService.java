package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.controller.event.SocketEvent;
import com.ladbrokescoral.oxygen.timeline.api.model.dto.out.PostMessageDto;
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
import org.springframework.messaging.Message;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class OnConnectMessageService {
  private final PostMessageService postMessageService;
  private final ModelMapper modelMapper;

  public Message<String> initialPosts() {
    return MessageContent.withPayload(SocketEvent.POST_PAGE.toString(), findFirstPage());
  }

  private Page<PostMessageDto> findFirstPage() {
    Page<PostMessage> firstPagePosts = postMessageService.findPage(0);
    if (firstPagePosts.getTotalElements() == 0) {
      return new CustomPageImpl<>(Collections.emptyList());
    } else {
      return new CustomPageImpl<>(
          modelMapper.map(
              firstPagePosts.getContent(),
              new TypeToken<Collection<PostMessageDto>>() {}.getType()),
          PageRequest.of(0, firstPagePosts.getPageable().getPageSize()),
          firstPagePosts.getTotalElements());
    }
  }
}
