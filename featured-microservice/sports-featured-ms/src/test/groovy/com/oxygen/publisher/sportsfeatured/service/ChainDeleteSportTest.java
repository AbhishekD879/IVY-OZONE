package com.oxygen.publisher.sportsfeatured.service;

import static com.oxygen.publisher.sportsfeatured.context.SportsSocketMessages.FEATURED_STRUCTURE_CHANGED;
import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;
import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.api.EntityLock;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.PageCacheUpdate;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import com.oxygen.publisher.translator.AbstractWorker;
import com.oxygen.publisher.translator.DiagnosticService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ChainDeleteSportTest {

  public static final String PAGE_ID = "h1";
  public static final PageRawIndex.GenerationKey GENERATION_ID =
      PageRawIndex.GenerationKey.fromPage(PAGE_ID, 10);
  public static final PageRawIndex thisPageIndex = PageRawIndex.fromGenerationKey(GENERATION_ID);
  public static final String chainId = "TEST_CHAIN";

  private SportsChainFactory testedService;
  private FeaturedModel sportSample;
  private FeaturedModel emptyModel;

  @Mock EntityLock locker;
  @Mock SportsMiddlewareContext sportsContext;
  @Mock ObjectMapper objectMapper;
  SocketIOServer socketIOServer;
  BroadcastOperations broadcastOperations;
  @Mock SportsCachedData featuredCachedData;
  @Mock DiagnosticService diagnosticService;
  @Mock SportsSessionContext sportsSessionContext;

  @Before
  public void init() {
    testedService =
        new SportsChainFactory(
            sportsContext, objectMapper, diagnosticService, sportsSessionContext);
    socketIOServer = mock(SocketIOServer.class);
    broadcastOperations = mock(BroadcastOperations.class);
    sportSample =
        FeaturedModel.builder()
            .pageId(PAGE_ID)
            .title("TEST_SPORT")
            .showTabOn("showTabOn")
            .visible(true)
            .directiveName("directiveName")
            .build();
    sportSample.addModule(mock(AbstractFeaturedModule.class));
    emptyModel =
        FeaturedModel.builder()
            .pageId(PAGE_ID)
            .title("TEST_SPORT")
            .showTabOn("showTabOn")
            .visible(true)
            .directiveName("directiveName")
            .build();

    given(locker.getEntityGUID()).willReturn(chainId);
  }

  private void notifierCondition() {
    given(sportsContext.socketIOServer()).willReturn(socketIOServer);
    when(socketIOServer.getRoomOperations(anyString())).thenReturn(broadcastOperations);
  }

  private void deleteSportPageConditions() {
    given(sportsContext.getFeaturedCachedData()).willReturn(featuredCachedData);
    given(featuredCachedData.getStructure(thisPageIndex)).willReturn(sportSample);
  }

  private AbstractWorker<String, PageRawIndex> deleteSportsPage_Coworker() {
    return testedService.and(
        locker,
        (thisWorker, version) -> {
          assertEquals(GENERATION_ID.toString(), version);
          deleteSportPageConditions();
          notifierCondition();
          thisWorker.accept(thisPageIndex, () -> testedService.deleteSportPage(version));
        });
  }

  private AbstractWorker<FeaturedModel, FeaturedModel> createNotifier_Coworker() {
    return testedService.and(
        locker,
        (thisWorker, model) -> {
          assertEquals(sportSample, model);
          notifierCondition();
          thisWorker.accept(model, () -> testedService.clientStructureChangeNotifier());
        });
  }

  @Test
  public void deleteSportPage_OK() {
    deleteSportsPage_Coworker().start(GENERATION_ID.toString());

    then(sportsContext).should(times(1)).applyWorkingCache(new PageCacheUpdate(GENERATION_ID));
    then(broadcastOperations)
        .should(times(1))
        .sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), emptyModel);
  }

  @Test
  public void clientChangeNotifier_OK() {
    this.createNotifier_Coworker().start(sportSample);

    then(broadcastOperations)
        .should(times(1))
        .sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), sportSample);
  }
}
