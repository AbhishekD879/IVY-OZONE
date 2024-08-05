package com.coral.oxygen.edp.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import java.math.BigInteger;
import java.util.Date;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class LiveServMessageConverter {

  private final OxyJsonMapper oxyJsonMapper;

  private final Map<BigInteger, BigInteger> selectionToMarketIdMap = new ConcurrentHashMap<>();

  public void addSelectionToMarketIdMapping(BigInteger selectionId, BigInteger marketId) {
    selectionToMarketIdMap.put(selectionId, marketId);
  }

  public void removeSelectionToMarketIdMapping(BigInteger selectionId) {
    selectionToMarketIdMap.remove(selectionId);
  }

  public BaseObject convert(MessageEnvelope messageEnvelope) {
    BaseObject baseObject = new BaseObject();
    String messageCode = messageEnvelope.getMessage().getMessageCode();
    String jsonData = messageEnvelope.getMessage().getJsonData();

    baseObject.setPublishedDate(new Date());
    String type = messageCode.substring(29, 34);
    Integer eventId = (int) messageEnvelope.getEventId();
    BigInteger subchannelId = new BigInteger(messageCode.substring(34, 44));
    baseObject.setType(type);
    long channelId = Long.parseLong(messageEnvelope.getChannel().substring(6));
    switch (type) {
      case "EVENT":
        baseObject.setEvent(oxyJsonMapper.read(jsonData, BaseObject.Event.class));
        baseObject.getEvent().setEventId(eventId);
        baseObject
            .getEvent() //
            .setMarket(new BaseObject.Market().setOutcome(new BaseObject.Outcome()));
        break;
      case "EVMKT":
        baseObject.setEvent(
            new BaseObject.Event() //
                .setEventId(eventId) //
                .setMarket(
                    oxyJsonMapper
                        .read(jsonData, BaseObject.Market.class)
                        .setMarketId(subchannelId) //
                        .setOutcome(new BaseObject.Outcome())));
        baseObject.getEvent().setEventId(eventId);
        break;
      case "SELCN":
        baseObject.setEvent(new BaseObject.Event()); //
        baseObject
            .getEvent()
            .setEventId(eventId) //
            .setMarket(new BaseObject.Market()); //
        baseObject
            .getEvent()
            .getMarket()
            .setOutcome(
                oxyJsonMapper
                    .read(jsonData, BaseObject.Outcome.class) //
                    .setOutcomeId(subchannelId)); //
        baseObject
            .getEvent()
            .getMarket()
            .setMarketId( //
                baseObject.getEvent().getMarket().getOutcome().getEvMktId()); //
        baseObject.getEvent().getMarket().getOutcome().setEvMktId(null);

        baseObject
            .getEvent()
            .getMarket()
            .getOutcome()
            .setPrice(
                new BaseObject.Price()
                    .setLpDen(baseObject.getEvent().getMarket().getOutcome().getLpDen())
                    .setLpNum(baseObject.getEvent().getMarket().getOutcome().getLpNum()));
        break;
      case "PRICE", "PSTRM":
        BigInteger marketId = selectionToMarketIdMap.get(channelId);
        baseObject.setEvent(
            new BaseObject.Event() //
                .setEventId(eventId) //
                .setMarket(
                    new BaseObject.Market()
                        .setMarketId(marketId == null ? null : marketId) //
                        .setOutcome(
                            new BaseObject.Outcome() //
                                .setOutcomeId(subchannelId) //
                                .setPrice(oxyJsonMapper.read(jsonData, BaseObject.Price.class)))));
        break;
      case "SCBRD":
        baseObject.setEvent(
            new BaseObject.Event() //
                .setEventId(eventId) //
                .setScoreboard(oxyJsonMapper.read(jsonData, BaseObject.Scoreboard.class)));
        break;
      case "CLOCK":
        baseObject.setEvent(
            new BaseObject.Event()
                .setEventId(eventId) //
                .setClock(oxyJsonMapper.read(jsonData, BaseObject.Clock.class)));

        baseObject.getEvent().getClock().setEvId(null);
        break;
      default:
        log.debug(
            "Invalid message for type {} , \n BODY-> {}",
            baseObject.getType(),
            messageEnvelope.getMessage());
        return null;
    }
    return baseObject;
  }
}
