package com.oxygen.publisher.inplay.service;

import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.inplay.InplayServiceRegistry;
import com.oxygen.publisher.model.*;
import com.oxygen.publisher.service.ConsumerDataService;
import java.io.IOException;
import java.util.List;
import java.util.function.Consumer;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import retrofit2.Call;
import retrofit2.Response;

@Slf4j
public class InplayDataServiceImpl extends ConsumerDataService implements InplayDataService {

  @Setter private InplayServiceRegistry serviceRegistry;

  private InplayConsumerApi inplayConsumerApi() {
    return serviceRegistry.getInplayConsumerApi();
  }

  @Trace(metricName = "GET-Generation", dispatcher = true)
  @Override
  public void getLastGeneration(Consumer<String> onSuccess) {
    log.info("[InplayDataServiceImpl::getLastGeneration]");
    doCall(inplayConsumerApi().getVersion(), onSuccess);
  }

  @Trace(metricName = "GET-Inplay-model", dispatcher = true)
  @Override
  public void getInPlayModel(String generation, Consumer<InPlayData> onSuccess) {
    log.info("[InplayDataServiceImpl::getInPlayModel version->{}.]", generation);
    doCall(inplayConsumerApi().getInPlayModel(generation), onSuccess);
  }

  @Trace(metricName = "GET-Sports-ribbon", dispatcher = true)
  @Override
  public void getSportsRibbon(String generation, Consumer<SportsRibbon> onSuccess) {
    log.info("[InplayDataServiceImpl::getSportsRibbon version->{}.]", generation);
    doCall(inplayConsumerApi().getSportsRibbon(generation), onSuccess);
  }

  @Trace(metricName = "GET-Inplay-cache", dispatcher = true)
  @Override
  public void getInPlayCache(String generation, Consumer<InPlayCache> onSuccess) {
    log.info("[InplayDataServiceImpl::getInPlayCache version->{}.]", generation);
    doCall(inplayConsumerApi().getInPlayCache(generation), onSuccess);
  }

  @Trace(metricName = "GET-Sport-segment", dispatcher = true)
  @Override
  public void getSportSegment(String storageKey, Consumer<SportSegment> onSuccess) {
    log.info("[InplayDataServiceImpl::getSportSegment {}.]", storageKey);
    doCall(inplayConsumerApi().getSportSegment(storageKey), onSuccess);
  }

  @Trace(metricName = "GET-Virtual-Sports", dispatcher = true)
  @Override
  public void getVirtualSport(String generation, Consumer<List<VirtualSportEvents>> onSuccess) {
    log.info("[InplayDataServiceImpl::getSportSegment {}.]", generation);
    doCall(inplayConsumerApi().getVirtualSports(generation), onSuccess);
  }

  private <R> void doCall(Call<R> call, Consumer<R> onSuccess) {
    try {
      Response<R> response = call.execute();
      processResponse(response, onSuccess);
    } catch (IOException e) {
      processFailure(call, e, onSuccess);
    }
  }
}
