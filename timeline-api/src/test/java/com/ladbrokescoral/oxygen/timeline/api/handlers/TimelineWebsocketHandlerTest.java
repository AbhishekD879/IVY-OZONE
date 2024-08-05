package com.ladbrokescoral.oxygen.timeline.api.handlers;

import com.ladbrokescoral.oxygen.timeline.api.model.Template;
import com.ladbrokescoral.oxygen.timeline.api.model.message.CampaignMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.TimelineSelectionEvent;
import com.ladbrokescoral.oxygen.timeline.api.repository.CampaignRepository;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.LoadNextPageMessageService;
import com.ladbrokescoral.oxygen.timeline.api.service.OnConnectMessageService;
import com.ladbrokescoral.oxygen.timeline.api.service.PostMessageService;
import com.ladbrokescoral.oxygen.timeline.api.service.impl.PostMessageServiceImpl;
import java.net.URI;
import java.net.URISyntaxException;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.client.ReactorNettyWebSocketClient;
import org.springframework.web.reactive.socket.client.WebSocketClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@DirtiesContext
public class TimelineWebsocketHandlerTest {
  @LocalServerPort private String port;
  @MockBean private PostRepository postRepository;
  @MockBean private CampaignRepository campaignRepository;

  @Autowired
  private PostMessageService postMessageService =
      new PostMessageServiceImpl(postRepository, campaignRepository);

  @Autowired private OnConnectMessageService onConnectMessageService;
  @Autowired private LoadNextPageMessageService loadNextPageMessageService;

  @Autowired
  TimelineWebsocketHandler timelineWebsocketHandler =
      new TimelineWebsocketHandler(onConnectMessageService, loadNextPageMessageService);

  @Test
  public void testPing() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> "2");
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(actualRef.get().size(), count + 1);
  }

  @Test
  public void testDisconnect() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> "0,[\"DISCONNECT\"]");
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(actualRef.get().size(), count + 1);
  }

  @Test
  public void testExceptionCase1() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    int count = 1;
    Flux<String> input = Flux.range(0, count).map(index -> "4");
    Mockito.when(postRepository.findByCampaignId(Mockito.anyString()))
        .thenReturn(
            List.of(
                PostMessage.builder()
                    .template(new Template())
                    .campaignId("1")
                    .campaignName("campign1")
                    .headerText("header")
                    .isSpotlight(false)
                    .isVerdict(false)
                    .selectionEvent(new TimelineSelectionEvent())
                    .build()));
    CampaignMessage message = new CampaignMessage();
    message.setBrand("bma");
    message.setDisplayFrom(Instant.now().minus(1, ChronoUnit.DAYS));
    message.setDisplayTo(Instant.now().plus(1, ChronoUnit.DAYS));
    message.setPageSize(1);
    message.setId("1");

    Mockito.when(campaignRepository.findAll()).thenReturn(List.of(message));
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(count + 1, actualRef.get().size());
  }

  @Test
  public void testLoadPostPageCase1() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    String inputString =
        "42[\"LOAD_POST_PAGE\",{\"from\":{\"id\":\"6461fd3d68fd1f579bd47fd5\",\"timestamp\":\"2023-05-15T09:37:01.672Z\"}}]";
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> inputString);
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(count + 1, actualRef.get().size());
  }

  @Test
  public void testLoadPostPageCase2() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    Mockito.when(campaignRepository.findAll()).thenReturn(getCampaignMessages());
    Mockito.when(postRepository.findByCampaignId("64635f010352a45a43c8930b"))
        .thenReturn(getPostMessages());
    String inputString =
        "42[\"LOAD_POST_PAGE\",{\"from\":{\"id\":\"64635fc00352a45a43c89314\",\"timestamp\":\"2023-05-16T10:49:52.078Z\"}}]";
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> inputString);
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(count + 1, actualRef.get().size());
  }

  @Test
  public void testLoadPostPageCase3() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    Mockito.when(campaignRepository.findAll()).thenReturn(getCampaignMessages());
    Mockito.when(postRepository.findByCampaignId("64635f010352a45a43c8930b"))
        .thenReturn(getPostMessagesForCase3());
    String inputString =
        "42[\"LOAD_POST_PAGE\",{\"from\":{\"id\":\"64635fc00352a45a43c89314\",\"timestamp\":\"2023-05-16T10:49:52.078Z\"}}]";
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> inputString);
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(count + 1, actualRef.get().size());
  }

  @Test
  public void testLoadPostPageCase4() throws URISyntaxException {
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    Iterable<CampaignMessage> campaignMessages = getCampaignMessages();
    campaignMessages.forEach(
        campaignMessage -> {
          campaignMessage.setDisplayFrom(Instant.now());
          campaignMessage.setDisplayTo(Instant.now().plusSeconds(180));
        });
    Mockito.when(campaignRepository.findAll()).thenReturn(campaignMessages);
    Mockito.when(postRepository.findByCampaignId("64635f010352a45a43c8930b"))
        .thenReturn(getPostMessages());
    String inputString =
        "42[\"LOAD_POST_PAGE\",{\"from\":{\"id\":\"64635fc00352a45a43c89314\",\"timestamp\":\"2023-05-16T10:49:52.078Z\"}}]";
    int count = 2;
    Flux<String> input = Flux.range(0, count).map(index -> inputString);
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .thenMany(
                        session
                            .receive()
                            .take(count + 1)
                            .map(WebSocketMessage::getPayloadAsText)
                            .log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .then())
        .block(Duration.ofSeconds(10L));
    Assert.assertNotNull(actualRef.get());
    Assert.assertEquals(count + 1, actualRef.get().size());
  }

  @Test
  public void testTimeout() throws InterruptedException, URISyntaxException {

    CountDownLatch latch = new CountDownLatch(1);
    WebSocketClient client = new ReactorNettyWebSocketClient();
    AtomicReference<List<String>> actualRef = new AtomicReference<>();
    Flux<String> input = Flux.interval(Duration.ofSeconds(61)).map(index -> "2");
    client
        .execute(
            getUrl("/socket.io"),
            session ->
                session
                    .send(input.map(session::textMessage))
                    .timeout(Duration.ofSeconds(61), Mono.empty())
                    .thenMany(
                        session.receive().take(1).map(WebSocketMessage::getPayloadAsText).log())
                    .collectList()
                    .doOnNext(actualRef::set)
                    .doOnNext(System.out::println)
                    .then()
                    .log())
        .subscribe();

    latch.await(62, TimeUnit.SECONDS);
    Assert.assertNotNull(actualRef.get());
  }

  protected URI getUrl(String path) throws URISyntaxException {
    return new URI("ws://localhost:" + this.port + path);
  }

  public Iterable<CampaignMessage> getCampaignMessages() {
    List<CampaignMessage> campaignMessages = new ArrayList<>();
    CampaignMessage message = new CampaignMessage();
    message.setId("64635f010352a45a43c8930b");
    message.setCreatedDate(Instant.parse("2023-05-16T10:46:46.188221900Z"));
    message.setBrand("ladbrokes");
    message.setDisplayFrom(Instant.parse("2023-05-03T10:20:29.016Z"));
    message.setDisplayTo(Instant.parse("2023-05-30T10:20:29Z"));
    message.setPageSize(2);
    campaignMessages.add(message);
    return campaignMessages;
  }

  public List<PostMessage> getPostMessages() {
    List<PostMessage> postMessages = new ArrayList<>();

    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("64635f010352a45a43c8930b");
    postMessage.setCampaignName("");
    postMessage.setPinned(false);
    postMessage.setText(null);
    postMessage.setHeaderText(null);
    postMessage.setTemplate(getTemplate());
    postMessage.setId("64635f0c0352a45a43c8930d");
    postMessage.setCreatedDate(Instant.parse("2023-05-16T10:47:18.330326500Z"));
    postMessage.setBrand("ladbrokes");
    postMessage.setSpotlight(false);
    postMessage.setVerdict(false);
    postMessage.setSelectionEvent(null);

    PostMessage postMessage2 = PostMessage.builder().build();
    postMessage2.setCampaignId("64635f010352a45a43c8930b");
    postMessage2.setCampaignName("");
    postMessage2.setPinned(false);
    postMessage2.setText(null);
    postMessage2.setHeaderText(null);
    postMessage2.setTemplate(getTemplate());
    postMessage2.setId("64635fc00352a45a43c89314");
    postMessage2.setCreatedDate(Instant.parse("2023-05-16T10:50:15.715562300Z"));
    postMessage2.setBrand("ladbrokes");
    postMessage2.setSpotlight(false);
    postMessage2.setVerdict(false);
    postMessage2.setSelectionEvent(null);

    PostMessage postMessage3 = PostMessage.builder().build();
    postMessage3.setCampaignId("64635f010352a45a43c8930b");
    postMessage3.setCampaignName("");
    postMessage3.setPinned(false);
    postMessage3.setText(null);
    postMessage3.setHeaderText(null);
    postMessage3.setTemplate(getTemplate());
    postMessage3.setId("64635f580352a45a43c89311");
    postMessage3.setCreatedDate(Instant.parse("2023-05-16T10:48:08.036991100Z"));
    postMessage3.setBrand("ladbrokes");
    postMessage3.setSpotlight(false);
    postMessage3.setVerdict(false);
    postMessage3.setSelectionEvent(null);

    postMessages.add(postMessage);
    postMessages.add(postMessage3);
    postMessages.add(postMessage2);
    return postMessages;
  }

  public List<PostMessage> getPostMessagesForCase3() {
    List<PostMessage> postMessages = new ArrayList<>();

    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("64635f010352a45a43c8930b");
    postMessage.setCampaignName("");
    postMessage.setPinned(false);
    postMessage.setText(null);
    postMessage.setHeaderText(null);
    postMessage.setTemplate(getTemplate());
    postMessage.setId("64635f0c0352a45a43c8930d");
    postMessage.setCreatedDate(Instant.parse("2023-05-16T10:50:15.715562300Z"));
    postMessage.setBrand("ladbrokes");
    postMessage.setSpotlight(false);
    postMessage.setVerdict(false);
    postMessage.setSelectionEvent(null);

    PostMessage postMessage2 = PostMessage.builder().build();
    postMessage2.setCampaignId("64635f010352a45a43c8930b");
    postMessage2.setCampaignName("");
    postMessage2.setPinned(false);
    postMessage2.setText(null);
    postMessage2.setHeaderText(null);
    postMessage2.setTemplate(getTemplate());
    postMessage2.setId("64635fc00352a45a43c89314");
    postMessage2.setCreatedDate(Instant.parse("2023-05-16T10:47:18.330326500Z"));
    postMessage2.setBrand("ladbrokes");
    postMessage2.setSpotlight(false);
    postMessage2.setVerdict(false);
    postMessage2.setSelectionEvent(null);
    postMessages.add(postMessage);
    postMessages.add(postMessage2);
    return postMessages;
  }

  public Template getTemplate() {
    Template templateDto = new Template();
    templateDto.setId("6038d77731f2881e7784978e");
    templateDto.setName("Welcome/Goodbye Message!");
    templateDto.setPostIconSvgId("LadsLoungeFootball");
    templateDto.setHeaderIconSvgId(null);
    templateDto.setHeaderText("Welcome To Ladbrokes Lounge");
    templateDto.setYellowHeaderText(" ");
    templateDto.setSubHeader("Sub Header");
    templateDto.setEventId("239317570");
    templateDto.setSelectionId("1895068122");
    templateDto.setPrice(null);
    templateDto.setBetPromptHeader("Bet promt");
    templateDto.setPostHref(
        "/horse-racing/horse-racing-live/kempton/18-30-kempton/239317570/win-or-each-way");
    templateDto.setText(
        "<p>Good afternoon and welcome to the Ladbrokes Lounge. Your one-stop shop for the latest news, odds and offers from all of today's matches. We'll be with you from now until 5pm guiding you through another busy day of domestic football</p>");
    templateDto.setYellowSubHeaderBackground(false);
    templateDto.setShowLeftSideRedLine(true);
    templateDto.setShowLeftSideBlueLine(false);
    templateDto.setShowTimestamp(true);
    templateDto.setShowRedirectArrow(true);
    templateDto.setShowRacingPostLogoInHeader(true);
    templateDto.setSpotlightTemplate(false);
    templateDto.setVerdictTemplate(false);
    templateDto.setTopRightCornerImagePath("");
    return templateDto;
  }
}
