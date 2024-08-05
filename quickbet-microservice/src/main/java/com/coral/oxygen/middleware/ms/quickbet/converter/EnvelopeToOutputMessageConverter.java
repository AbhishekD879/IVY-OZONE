package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv.*;
import com.google.gson.Gson;
import com.ladbrokescoral.scoreboards.parser.api.BipParserFactory;
import com.ladbrokescoral.scoreboards.parser.model.BipComment;
import java.util.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class EnvelopeToOutputMessageConverter extends BaseConverter<Envelope, List<OutputMessage>> {
  private Gson gson;

  @Autowired
  public EnvelopeToOutputMessageConverter(Gson gson) {
    this.gson = gson;
  }

  @Override
  public List<OutputMessage> populateResult(Envelope envelope, List<OutputMessage> list) {
    OutputMessage outputMessage = buildMessage(envelope);
    list.add(outputMessage);

    Map<String, Object> message = (Map) outputMessage.getMessage();
    Optional<BipComment> maybeBipComment =
        Optional.ofNullable(message.get("names"))
            .map(names -> (Map<String, String>) names)
            .flatMap(names -> Optional.ofNullable(names.get("en")))
            .flatMap(this::tryParse);

    if (ChannelType.sEVENT.name().equals(outputMessage.getChannel().getType())
        && maybeBipComment.isPresent()) {
      BipComment bipComment = maybeBipComment.get();
      OutputMessage scbrdOutputMessage = buildScbrdMessage(outputMessage, bipComment);
      list.add(scbrdOutputMessage);

      String parsedName = bipComment.getEventName();
      ((Map<String, String>) message.get("names")).put("en", parsedName);
    }
    return list;
  }

  private Optional<BipComment> tryParse(String eventName) {
    BipComment bipComment = BipParserFactory.getUnknownCategoryParser().parse(eventName);
    if (bipComment.getEventName() != null) {
      return Optional.of(bipComment);
    }
    return Optional.empty();
  }

  @Override
  protected List<OutputMessage> createTarget() {
    return new ArrayList<>();
  }

  OutputMessage buildMessage(Envelope envelope) {
    MessageEnvelope messageEnvelope = (MessageEnvelope) envelope;
    Map<String, String> message =
        gson.fromJson(messageEnvelope.getMessage().getJsonData(), Map.class);
    return new OutputMessage(
        messageEnvelope.getType(),
        new OutputEvent(messageEnvelope.getEventId()),
        buildChannel(messageEnvelope.getMessage().getMessageCode().substring(1, 17)),
        buildChannel(messageEnvelope.getMessage().getMessageCode().substring(28, 44)),
        message);
  }

  private OutputChannel buildChannel(String code) {
    return new OutputChannel(code, Long.parseLong(code.substring(6)), code.substring(0, 6));
  }

  OutputMessage buildScbrdMessage(OutputMessage source, BipComment bipComment) {
    return new OutputMessage()
        .withChannel(
            new OutputChannel(
                source
                    .getChannel()
                    .getName()
                    .replace(ChannelType.sEVENT.name(), ChannelType.sSCBRD.getName()),
                source.getChannel().getId(),
                source
                    .getChannel()
                    .getType()
                    .replace(ChannelType.sEVENT.name(), ChannelType.sSCBRD.getName())))
        .withEvent(new OutputEvent(source.getEvent().getId()))
        .withSubChannel(
            new OutputChannel(
                source
                    .getSubChannel()
                    .getName()
                    .replace(ChannelType.sEVENT.name(), ChannelType.sSCBRD.getName()),
                source.getSubChannel().getId(),
                source
                    .getSubChannel()
                    .getType()
                    .replace(ChannelType.sEVENT.name(), ChannelType.sSCBRD.getName())))
        .withType(source.getType())
        .withMessage(buildScoreboard(bipComment));
  }

  private Scoreboard buildScoreboard(BipComment bipComment) {
    Scoreboard scoreboard = new Scoreboard();
    if (bipComment.getPlayerHomeComment() != null
        && bipComment.getPlayerBComment() != null
        && bipComment.getPlayerHomeComment().getScore() != null
        && bipComment.getPlayerAwayComment().getScore() != null) {
      scoreboard.setAll(
          Arrays.asList(
              ScoreboardDetails.createHomeEventDetails(
                  bipComment.getPlayerHomeComment().getScore()),
              ScoreboardDetails.createAwayEventDetails(
                  bipComment.getPlayerAwayComment().getScore())));
    }
    if (bipComment.getPlayerHomeComment() != null
        && bipComment.getPlayerAwayComment() != null
        && bipComment.getPlayerHomeComment().getCurrentPoints() != null
        && bipComment.getPlayerAwayComment().getCurrentPoints() != null) {
      scoreboard.setCurrent(
          Arrays.asList(
              ScoreboardDetails.createHomeEventDetails(
                  bipComment.getPlayerHomeComment().getCurrentPoints()),
              ScoreboardDetails.createAwayEventDetails(
                  bipComment.getPlayerAwayComment().getCurrentPoints())));
    }
    if (bipComment.getPlayerHomeComment() != null
        && bipComment.getPlayerAwayComment() != null
        && bipComment.getPlayerHomeComment().getPeriodScore() != null
        && bipComment.getPlayerAwayComment().getPeriodScore() != null) {
      scoreboard.setSubperiod(
          Arrays.asList(
              ScoreboardDetails.createHomeEventDetails(
                  bipComment.getPlayerHomeComment().getPeriodScore()),
              ScoreboardDetails.createAwayEventDetails(
                  bipComment.getPlayerAwayComment().getPeriodScore())));
    }
    return scoreboard;
  }
}
