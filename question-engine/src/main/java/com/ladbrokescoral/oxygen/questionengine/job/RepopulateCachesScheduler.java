package com.ladbrokescoral.oxygen.questionengine.job;

import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.UpsellDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.service.impl.QuizCacheDataSourceImpl;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import io.vavr.control.Option;
import io.vavr.control.Try;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.Cache;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static org.jboss.logging.NDC.peek;

@Service
@Slf4j
@RequiredArgsConstructor
@ConditionalOnProperty("application.cachingEnabled")
public class RepopulateCachesScheduler {
  private final CmsService cmsService;
  private final UpsellService upsellService;
  private final QuizService quizService;
  private final ModelMapper modelMapper;
  private final ApplicationProperties applicationProperties;

  @Value("#{cacheManager.getCache('liveQuizCache')}")
  private Cache liveQuizCache;

  @Value("#{cacheManager.getCache('quizHistoryCache')}")
  private Cache quizHistoryCache;

  @Value("#{cacheManager.getCache('upsellCache')}")
  private Cache upsellCache;

  private final QuizCacheDataSourceImpl quizCacheDataSource;

  private static final String QUIZ_HISTORY_MAP = "quizHistoryMap";

  @Scheduled(fixedDelayString = "${application.quizCachingPeriod}")
  public void populateHistoryCaches() {
    List<QuizDto> liveQuizzes = new ArrayList<>();
    List<QuizHistory> quizHistory;

    Map<String,QuizHistory> quizHistoryMapCache = quizCacheDataSource.getQuizHistory();
    if(null!=quizHistoryMapCache && quizHistoryMapCache.size()>0){
       Collection<QuizHistory> quizHistoryCollection =  quizHistoryMapCache.values();
       quizHistory = new ArrayList<>(quizHistoryCollection);
    }else{
      log.debug("calling cms to fetch quizHistory");
      quizHistory = cmsService.findHistory(applicationProperties.getHistoryPreviousCacheSize());
    }

    for (QuizHistory history : quizHistory) {
      String sourceId = history.getSourceId();
      AppQuizHistoryDto historyDto = modelMapper.map(history, AppQuizHistoryDto.class);
      QuizDto live = historyDto.getLive();
      if (history.getLive() != null) {
        liveQuizzes.add(live);
        upsellService.findUpsellFor(live).ifPresent(live::setUpsell);
      }

      quizHistoryCache.put(sourceId, historyDto);
      log.info("QuizHistory cache was updated. Key: {}, Live Quiz: {}, Previous Quizzes ({}): [{}]",
          sourceId,
          live != null ? live.getId() : "Does not exist",
          historyDto.getPrevious().size(),
          historyDto.getPrevious().stream()
              .map(QuizDto::getId)
              .collect(Collectors.joining(", "))
      );
    }

    liveQuizCache.put("$LIVE_QUIZZES", liveQuizzes);
  }

  @Scheduled(fixedDelayString = "${application.upsellCachingPeriod}")
  public void populateUpsellCache() {
    quizService.findLiveQuizzes()
        .stream()
        .map(live -> modelMapper.map(live, QuizDto.class))
        .forEach(this::updateUpsellCache);
  }

  private void updateUpsellCache(QuizDto quiz) {
    UpsellDto oldUpsell = upsellCache.get(quiz.getSourceId(), UpsellDto.class);
    upsellCache.evict(quiz.getSourceId());

    Try.of(() -> upsellService.findUpsellFor(quiz))
            .onFailure(ex -> log.error("UpsellService.findUpsellFor for Live Quiz with Source Id '{}'. Reason: {}", quiz.getSourceId(), ex))
            .toOption()
            .flatMap(Option::ofOptional)
            .orElse(() -> Option.of(oldUpsell).peek(upsell -> log.warn("Upsell for Live Quiz with Source Id '{}' might be outdated", quiz.getSourceId())))
            .peek(upsell -> upsellCache.put(quiz.getSourceId(), upsell))
            .peek(upsell -> log.info("Upsell cache was repopulated. Key: {}, Value: {}", quiz.getSourceId(), upsell))
            .onEmpty(() -> log.info("No Upsell cache entry created for Live Quiz with Source Id: {}", quiz.getSourceId()));

  }
}
