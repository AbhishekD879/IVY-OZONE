package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.util.Util.*;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineChangelogRepository;
import com.mongodb.client.MongoCursor;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.bson.Document;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class TimelineChangeListener<E extends AbstractEntity> implements ApplicationRunner {

  private static final int NEW_RECORDS_WAIT_SECONDS = 5;
  private final TimelineChangelogRepository changelogRepository;
  private final List<TimelineChangelogSubscription<E>> subscriptions;

  @Async
  @Override
  public void run(ApplicationArguments args) {
    runForever(
        () -> {
          try (MongoCursor<Document> cursor = changelogRepository.stream().iterator()) {
            runForever(() -> watchNewRecords(cursor));
          } catch (Exception e) {
            log.error("Error while cursor tailoring", e);
          }
        });
  }

  @SneakyThrows
  private void watchNewRecords(MongoCursor<Document> cursor) {
    while (cursor.hasNext()) {
      Document document = cursor.next();
      TimelineChangelog<E> changelog = changelogRepository.convert(document);
      subscriptions.stream()
          .filter(subscription -> subscription.isSupportedChange(changelog))
          .forEach(executeSubscribeForChangeLog(changelog));
    }
    TimeUnit.SECONDS.sleep(NEW_RECORDS_WAIT_SECONDS);
  }

  private Consumer<TimelineChangelogSubscription<E>> executeSubscribeForChangeLog(
      TimelineChangelog<E> changelog) {
    return (TimelineChangelogSubscription<E> subscription) -> {
      try {
        subscription.subscribe(changelog);
      } catch (Exception e) {
        log.error("Exception on subscription: ", e);
      }
    };
  }
}
