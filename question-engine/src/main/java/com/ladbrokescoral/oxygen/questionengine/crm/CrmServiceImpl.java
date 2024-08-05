package com.ladbrokescoral.oxygen.questionengine.crm;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.CoinDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.PrizeDto;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.*;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.model.AwardStatus;
import com.ladbrokescoral.oxygen.questionengine.repository.AwardFailureRepository;
import com.ladbrokescoral.oxygen.questionengine.service.QuizHistoryService;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;
import org.springframework.stereotype.Service;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.jackson.JacksonConverterFactory;

import java.io.IOException;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
@Slf4j
public class CrmServiceImpl implements CrmService {

    @Value("${crm.type}")
    private String rewardComType;

    @Value("${crm.frontend}")
    private String frontend;

    @Value("${crm.brand}")
    private String brand;

    @Value("${crm.product}")
    private String product;

    @Value("${crm.source}")
    private String source;

    @Value("${crm.subSource}")
    private String subSource;

    @Value("${crm.error.codes}")
    private List<String> crmErrorCodes;

    private QuizHistoryService quizService;
    private AwardFailureRepository failureRepository;

    private final CrmEndPoint crmEndPoint;

    private static final String REWARD_ERROR_CODE = "ER000";

    private static final String REWARD_TYPE = "COIN";

    private static final String SUCCESS = "success";

    private static final String FAILURE = "failure";

    private static final String NONE = "none";

    @Autowired
    public CrmServiceImpl(@Value("${crm.base.url}") String baseUrl, OkHttpClient crmHttpClient, QuizHistoryService quizService, AwardFailureRepository failureRepository) {
        this.quizService = quizService;
        this.failureRepository = failureRepository;
        ObjectMapper mapper =
                Jackson2ObjectMapperBuilder.json()
                        .featuresToEnable(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY)
                        .build();
        this.crmEndPoint =
                new Retrofit.Builder()
                        .baseUrl(baseUrl)
                        .client(crmHttpClient)
                        .addConverterFactory(JacksonConverterFactory.create(mapper))
                        .build()
                        .create(CrmEndPoint.class);
    }

    public String getAward(QuizSubmitDto quizSubmitDto) {
        CoinRequest coinRequest = createAwardRequest(quizSubmitDto);
        log.info("CRM Award-API CoinRequest::: {}", coinRequest);
        if (!REWARD_TYPE.equalsIgnoreCase(coinRequest.getRewardDetails().getRewardType())) {
            log.info("In CMS PrizeType Configured NONE due to that skipping CRM-API Call {}", coinRequest);
            return NONE;
        }
        try {
            Call<CoinResponse> coinResponseCall = crmEndPoint.getRewardData(coinRequest);
            CoinResponse coinResponse = executeRequest(coinResponseCall, coinRequest).orElse(new CoinResponse());
            log.info("CRM Award-API CoinResponse::: {}", coinResponse);
            if (crmErrorCodes.stream().anyMatch(statusCode -> statusCode.contains(coinResponse.getRewardErrorCode()))) {
                log.info("process CoinResponse RewardErrorCode if {}", coinResponse.getRewardErrorCode());
                AwardStatus fssFailure = new AwardStatus(coinRequest.getRewardDetails().getRewardType(),
                        coinRequest.getRewardDetails().getRewardValue(), coinRequest.getRequestReferenceId(), createDateSubmittedOn(), coinRequest.getAccountName(),
                        coinResponse.getRewardErrorCode() + "_" + coinResponse.getRewardStatus(), "FSS");
                failureRepository.save(fssFailure);
                return FAILURE;
            } else if (REWARD_ERROR_CODE.equalsIgnoreCase(coinResponse.getRewardErrorCode())) {
                return SUCCESS;
            }
        } catch (Exception ex) {
            log.error("Error getAward CRM-API requestReferenceId {} message {}",
                    coinRequest.getRequestReferenceId(), ex.getMessage());
            AwardStatus fssFailure = new AwardStatus(coinRequest.getRewardDetails().getRewardType(),
                    coinRequest.getRewardDetails().getRewardValue(), coinRequest.getRequestReferenceId(), createDateSubmittedOn(),
                    coinRequest.getAccountName(), ex.getMessage(), "FSS");
            failureRepository.save(fssFailure);
            return FAILURE;
        }
        return FAILURE;
    }

    private <T> Optional<T> executeRequest(Call<T> call, CoinRequest coinRequest) throws IOException {
        Response<T> response = call.execute();
        if (!response.isSuccessful()) {
            log.error("Error executeRequest CRM-API Response code: {}, errorBody: {}.", response.code(), response.errorBody());
            AwardStatus fssFailure = new AwardStatus(coinRequest.getRewardDetails().getRewardType(),
                    coinRequest.getRewardDetails().getRewardValue(), coinRequest.getRequestReferenceId(), createDateSubmittedOn(),
                    coinRequest.getAccountName(), response.errorBody().toString(), "FSS");
            failureRepository.save(fssFailure);
            return Optional.empty();
        }
        return Optional.ofNullable(response.body());
    }

    private CoinRequest createAwardRequest(QuizSubmitDto quizSubmitDto) {
        CoinRequest coinRequest = new CoinRequest();
        AppQuizHistoryDto appHistory = quizService.findQuizHistory(quizSubmitDto.getSourceId());
        log.info("createAwardRequest CMS Live Quiz :::{}", appHistory.getLive());
        coinRequest.setAccountName(frontend + "_" + quizSubmitDto.getUsername());
        coinRequest.setRequestReferenceId(quizSubmitDto.getQuizId() + "_" + quizSubmitDto.getUsername());
        RewardAttributes rewardDetails = new RewardAttributes();
        rewardDetails.setRewardType(getRewardType(appHistory.getLive().getCorrectAnswersPrizes()));
        rewardDetails.setRewardValue(getRewardValue(appHistory.getLive().getCoin()));
        coinRequest.setRewardDetails(rewardDetails);
        List<ChannelInfo> rewardCommunication = new ArrayList<>();
        ChannelInfo channelInfo = new ChannelInfo();
        if (appHistory.getLive().getCoin() != null &&
                !StringUtils.isEmpty(appHistory.getLive().getCoin().getSiteCoreId())) {
            channelInfo.setType(rewardComType);
            channelInfo.setSitecoreTemplateId(appHistory.getLive().getCoin().getSiteCoreId());
        }
        channelInfo.setCustomCommunicationMap(channelInfo.asCommunicationMap(
                appHistory.getLive().getTitle(), quizSubmitDto.getUsername(),
                getRewardValue(appHistory.getLive().getCoin()),
                getRewardType(appHistory.getLive().getCorrectAnswersPrizes())));
        rewardCommunication.add(channelInfo);
        coinRequest.setRewardCommunication(rewardCommunication);
        PlayerSourceInfo playerSourceInfo = new PlayerSourceInfo();
        playerSourceInfo.setFrontend(frontend);
        playerSourceInfo.setBrand(brand);
        playerSourceInfo.setProduct(product);
        playerSourceInfo.setChannel(quizSubmitDto.getChannel());
        coinRequest.setPlayerSourceInfo(playerSourceInfo);
        CampaignSourceDetails campaignSourceDetails = new CampaignSourceDetails();
        campaignSourceDetails.setSource(source);
        campaignSourceDetails.setSubSource(subSource);
        campaignSourceDetails.setSourceId(quizSubmitDto.getQuizId());
        coinRequest.setCampaignSorceDetails(campaignSourceDetails);
        return coinRequest;
    }

    private String getRewardValue(CoinDto coin) {
        return (coin != null && coin.getValue() != null) ? coin.getValue().toString() : null;
    }

    private String getRewardType(Map<Integer, PrizeDto> correctAnswersPrizes) {
        return correctAnswersPrizes.size() != 0
                ? correctAnswersPrizes.get(0).getPrizeType().toString() : null;
    }

    private String createDateSubmittedOn() {
        Instant utcTime = Instant.now();
        ZonedDateTime currentTime = utcTime.atZone(ZoneId.systemDefault());
        return currentTime.toString();
    }

}
