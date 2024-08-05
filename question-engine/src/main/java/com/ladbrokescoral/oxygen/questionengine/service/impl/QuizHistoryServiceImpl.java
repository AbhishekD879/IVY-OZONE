package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Quiz;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Slf4j
@RequiredArgsConstructor
public class QuizHistoryServiceImpl implements QuizHistoryService {
    private final CmsService cmsService;
    private final UpsellService upsellService;
    private final ModelMapper modelMapper;
    private final ApplicationProperties properties;

    @Override
    @Cacheable(cacheNames = "quizHistoryCache", key = "#sourceId")
    public AppQuizHistoryDto findQuizHistory(String sourceId) {
        QuizHistory quizHistory = cmsService.findHistory(CmsService.normalizeSourceId(sourceId), properties.getHistoryPreviousCacheSize())
                .orElseThrow(() -> new NotFoundException("No Quiz for source id '%s' found", sourceId));
        AppQuizHistoryDto historyDto = modelMapper.map(quizHistory, AppQuizHistoryDto.class);

        if (historyDto.getLive() != null) {
            upsellService.findUpsellFor(historyDto.getLive()).ifPresent(historyDto.getLive()::setUpsell);
        }
        return historyDto;
    }

    @Override
    public List<Quiz> getAllQuizzes() {
        return cmsService.findAllQuizzes();
    }
}

