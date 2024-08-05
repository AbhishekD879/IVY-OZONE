package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineBigQueryChangelog;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineChangelogOperation;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Auditable;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryTimelineRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineChangelogRepository;
import java.time.Instant;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.bson.Document;
import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class TimelineMongoEventListener<T extends Auditable<?>>
    extends AbstractMongoEventListener<T> {
  private final BigQueryTimelineRepository bigQueryTimelineRepository;
  private final TimelineChangelogRepository changelogRepository;

  @Override
  public void onAfterSave(AfterSaveEvent<T> event) {
    Auditable<?> source = event.getSource();
    String username = source.getUpdatedByUserName();
    AbstractEntity content = source.content();
    TimelineChangelogOperation operation =
        content.getCreatedAt().equals(content.getUpdatedAt())
            ? TimelineChangelogOperation.INSERT
            : TimelineChangelogOperation.UPDATE;

    changelogRepository.save(
        new TimelineChangelog<>()
            .setOperation(operation)
            .setType(content.getClass())
            .setTimestamp(Instant.now())
            .setContentId(content.getId())
            .setContent(content));
    bigQueryTimelineRepository.save(
        new TimelineBigQueryChangelog()
            .setId(source.getId())
            .setUsername(username)
            .setCreatedDate(source.getUpdatedAt())
            .setType(source.content().getClass())
            .setOperation(operation)
            .setEntity(content));
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<T> event) {
    Document source = event.getSource();
    String username = findUsername();
    String contentId = source.get("_id").toString();

    changelogRepository.save(
        new TimelineChangelog<>()
            .setOperation(TimelineChangelogOperation.DELETE)
            .setType(event.getType())
            .setTimestamp(Instant.now())
            .setContentId(contentId));
    bigQueryTimelineRepository.save(
        new TimelineBigQueryChangelog()
            .setId(contentId)
            .setUsername(username)
            .setCreatedDate(Instant.now())
            .setType(event.getType())
            .setOperation(TimelineChangelogOperation.DELETE));
  }

  private String findUsername() {
    return Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
        .filter(Authentication::isAuthenticated)
        .map(Authentication::getPrincipal)
        .map(User.class::cast)
        .map(User::getEmail)
        .orElse("anonymous");
  }
}
