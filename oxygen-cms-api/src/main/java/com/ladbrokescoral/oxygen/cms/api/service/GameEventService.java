package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.GameEvent;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.Team;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.time.Instant;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Service
public class GameEventService {

  private static final String SITE_SERVE_EVENT_NAME_DELIMITER = "|";
  private static final String SITE_SERVE_EVENT_TEAM_DELIMITER = "vs";

  private final SiteServeApiProvider siteServeApiProvider;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String teamKitPath;
  private final TeamKitService teamKitService;

  public GameEventService(
      SiteServeApiProvider siteServeApiProvider,
      ImageService imageService,
      SvgImageParser svgImageParser,
      TeamKitService teamKitService,
      @Value("${images.teamKit.path}") String teamKitPath) {
    this.siteServeApiProvider = siteServeApiProvider;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.teamKitPath = teamKitPath;
    this.teamKitService = teamKitService;
  }

  public Optional<IncompleteGameEvent> findByEventId(String brand, String eventId) {
    return siteServeApiProvider
        .api(brand)
        .getEvent(eventId, true)
        .map(
            event ->
                IncompleteGameEvent.builder()
                    .eventId(eventId)
                    .startTime(Instant.parse(event.getStartTime()))
                    .homeTeamName(homeTeamName(event))
                    .awayTeamName(awayTeamName(event))
                    .build());
  }

  private String homeTeamName(Event event) {
    String eventName = event.getName();
    if (!StringUtils.containsIgnoreCase(eventName, SITE_SERVE_EVENT_TEAM_DELIMITER)) {
      log.warn("Couldn't parse Event Name correctly: {}", event.getName());
      return eventName;
    }

    String gameName = StringUtils.remove(eventName, SITE_SERVE_EVENT_NAME_DELIMITER);
    String teamName =
        gameName.substring(
            0, StringUtils.indexOfIgnoreCase(gameName, SITE_SERVE_EVENT_TEAM_DELIMITER));

    return StringUtils.trim(teamName);
  }

  private String awayTeamName(Event event) {
    String eventName = event.getName();
    if (!StringUtils.containsIgnoreCase(eventName, SITE_SERVE_EVENT_TEAM_DELIMITER)) {
      log.warn("Couldn't parse Event Name correctly: {}", event.getName());
      return eventName;
    }

    String gameName = StringUtils.remove(event.getName(), SITE_SERVE_EVENT_NAME_DELIMITER);
    String teamName =
        gameName.substring(
            StringUtils.lastIndexOfIgnoreCase(gameName, SITE_SERVE_EVENT_TEAM_DELIMITER)
                + SITE_SERVE_EVENT_TEAM_DELIMITER.length());
    return StringUtils.trim(teamName);
  }

  public GameEvent getGameEventById(Game game, String eventId) {
    return game.getEvents().stream()
        .filter(event -> event.getEventId().equals(eventId))
        .findFirst()
        .orElseThrow(NotFoundException::new);
  }

  public void uploadGameEventTeamImage(
      GameEvent gameEvent,
      String teamType,
      MultipartFile file,
      FileType fileType,
      String fileName,
      String brand) {
    if (FileType.SVG.equals(fileType)) {
      uploadSvgImageForGameEvent(file, gameEvent, teamType, fileName, brand);
    } else {
      uploadImageForGameEvent(file, gameEvent, teamType, fileName, brand);
    }
  }

  private void uploadImageForGameEvent(
      @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile file,
      GameEvent gameEvent,
      String teamType,
      String fileName,
      String brand) {
    Filename uploadedFile = uploadImage(file, fileName, brand);
    attachImageToTeam(gameEvent, teamType, uploadedFile);
  }

  private void uploadSvgImageForGameEvent(
      @ValidFileType("svg") MultipartFile file,
      GameEvent gameEvent,
      String teamType,
      String fileName,
      String brand) {
    Optional<Svg> svg = svgImageParser.parse(file);
    if (!svg.isPresent()) {
      throw new ValidationException("Svg image is invalid");
    }
    Filename uploadedFile = uploadImage(file, fileName, brand);
    attachImageToTeam(gameEvent, teamType, uploadedFile);
    teamKitService.saveTeamKit(getTeamByType(gameEvent, teamType), svg.get(), brand);
  }

  private Filename uploadImage(
      @ValidFileType({"jpeg", "png", "jpg"}) MultipartFile file, String fileName, String brand) {
    String name = StringUtils.isNotBlank(fileName) ? fileName : getFilename(file);

    return imageService
        .upload(brand, file, path(brand), name, null)
        .orElseThrow(() -> new IllegalStateException("Issue occurred during image uploading"));
  }

  public void removeImage(GameEvent gameEvent, String teamType) {
    Team team = getTeamByType(gameEvent, teamType);
    team.setTeamKitIcon(null);
  }

  private Team getTeamByType(GameEvent gameEvent, String teamType) {
    return teamType.equalsIgnoreCase("home") ? gameEvent.getHome() : gameEvent.getAway();
  }

  private void attachImageToTeam(GameEvent gameEvent, String teamType, Filename file) {
    Team team = getTeamByType(gameEvent, teamType);
    team.setTeamKitIcon(PathUtil.normalizedPath(file.getPath(), file.getFilename()));
  }

  private String getFilename(MultipartFile image) {
    return Optional.ofNullable(image.getOriginalFilename())
        .filter(img -> img.contains("."))
        .map(img -> StringUtils.substringBefore(img, "."))
        .orElseGet(image::getName);
  }

  private String path(String brand) {
    return StringUtils.endsWith(teamKitPath, "/")
        ? (teamKitPath + brand)
        : String.format("%s/%s", teamKitPath, brand);
  }
}
