package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.common.repository.AssetManagementRepository;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Pattern;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class AssetManagementService {

  private final AssetManagementRepository assetManagementRepository;

  @Value("${featured.scheduled.task.enabled:false}")
  private boolean isFeaturedTask;

  private static final String TEAM_SEPERATOR_REGEX = " vs | v ";
  private static final Pattern TEAM_SEPERATOR_PATTERN =
      Pattern.compile(TEAM_SEPERATOR_REGEX, Pattern.CASE_INSENSITIVE);

  public static final int TEAM_SIZE = 2;

  @Getter private Map<String, Optional<AssetManagement>> assets = new ConcurrentHashMap<>();
  private Set<String> lastGenerationTeams = new HashSet<>();

  @Autowired
  public AssetManagementService(AssetManagementRepository assetManagementRepository) {
    this.assetManagementRepository = assetManagementRepository;
  }

  public Iterable<AssetManagement> saveAll(List<AssetManagement> assetManagements) {
    assetManagementRepository.deleteAll();
    trimTeamsImage(assetManagements);
    Iterable<AssetManagement> assetManagementIterable =
        assetManagementRepository.saveAll(assetManagements);
    List<String> clonedLastGenerationTeams = List.copyOf(lastGenerationTeams);
    CompletableFuture.runAsync(
        () -> {
          clonedLastGenerationTeams.forEach(this::updateLocalAssets);
          List<String> removableKeys =
              assets.keySet().stream()
                  .filter(key -> !clonedLastGenerationTeams.contains(key))
                  .toList();
          removableKeys.forEach(assets::remove);
        });
    return assetManagementIterable;
  }

  private void updateLocalAssets(String teamKey) {
    String[] split = teamKey.split("#");
    Optional<AssetManagement> assetManagement = getAssetManagementFromRepo(split[0], split[1]);
    assetManagement.ifPresent(e -> assets.put(teamKey, assetManagement));
  }

  private void trimTeamsImage(List<AssetManagement> assets) {
    if (isFeaturedTask) {
      for (AssetManagement assetManagement : assets) {
        if (!assetManagement.isHighlightCarouselToggle()) {
          assetManagement.setTeamsImage(null);
        }
      }
    }
  }

  public Optional<AssetManagement> findByTeamNameAndSportId(String teamName, String sportId) {

    String teamKey = teamName + "#" + sportId;
    log.info("looking asset management data for {} in cache ", teamKey);
    lastGenerationTeams.add(teamKey);
    return Optional.ofNullable(assets.get(teamKey))
        .orElseGet(
            () -> {
              log.info(
                  "fetching asset management data for {} from DB and placing in cache", teamKey);
              Optional<AssetManagement> assetManagement =
                  getAssetManagementFromRepo(teamName, sportId);
              assetManagement.ifPresent(e -> assets.put(teamKey, assetManagement));
              return assetManagement;
            });
  }

  public Optional<AssetManagement> getAssetManagementFromRepo(String teamName, String sportId) {
    Optional<AssetManagement> assetManagement =
        assetManagementRepository.findByTeamNameIgnoreCaseAndSportId(
            teamName.toUpperCase(), Integer.parseInt(sportId));
    if (assetManagement.isEmpty()) {
      assetManagement = findBySecondaryName(teamName, sportId);
    }
    return assetManagement;
  }

  public void setAssetForTypeSegment(TypeSegment typeSegment, String sportId) {
    findByTeamNameAndSportId(typeSegment.getTypeName(), sportId)
        .ifPresent(typeSegment::setAssetManagement);
  }

  private Optional<AssetManagement> findBySecondaryName(String name, String sportId) {
    List<AssetManagement> assetManagements =
        assetManagementRepository.findBySportId(Integer.parseInt(sportId));
    if (!CollectionUtils.isEmpty(assetManagements)) {
      return assetManagements.stream()
          .filter(
              asset ->
                  !CollectionUtils.isEmpty(asset.getSecondaryNames())
                      && hasName(asset.getSecondaryNames(), name))
          .findAny();
    }
    return Optional.empty();
  }

  private boolean hasName(List<String> names, String name) {
    return names.stream().anyMatch(n -> n.equalsIgnoreCase(name));
  }

  public Iterable<AssetManagement> findAll() {
    return assetManagementRepository.findAll();
  }

  private List<String> getHomeAndAwayTeams(String teamName, Boolean isUsSport) {
    List<String> teams = new ArrayList<>();

    String[] names = TEAM_SEPERATOR_PATTERN.split(teamName.replace("|", ""));
    if (names.length == TEAM_SIZE) {
      teams = fetchHomeAndAwayTeamByType(isUsSport, names);
    }
    return teams;
  }

  private List<String> fetchHomeAndAwayTeamByType(Boolean isUsSport, String[] names) {
    List<String> teams = new ArrayList<>();
    if (Boolean.TRUE.equals(isUsSport)) {
      teams.add(names[1]);
      teams.add(names[0]);
    } else {
      teams.add(names[0]);
      teams.add(names[1]);
    }
    return teams;
  }

  private AssetManagement findAssetMetaData(String categoryId, String team) {
    Optional<AssetManagement> asset =
        findByTeamNameAndSportId(team.toUpperCase(Locale.ROOT), categoryId);
    return asset.orElse(null);
  }

  public void setAssetManagementMetaData(EventsModuleData eventsModuleData) {

    try {
      prepareAssetCache(eventsModuleData);
    } catch (Exception ex) {
      log.error("Failed to set assetManagement info", ex);
    }
  }

  private void prepareAssetCache(EventsModuleData eventsModuleData) {

    List<String> teams = getHomeAndAwayTeams(eventsModuleData.getName(), eventsModuleData.getUS());
    if (teams.size() == TEAM_SIZE) {
      // get by category for secondary names.
      eventsModuleData.setAssetManagements(
          getAssetsIfWeHaveForBothTeams(teams, eventsModuleData.getCategoryId()));
    }
  }

  private List<AssetManagement> getAssetsIfWeHaveForBothTeams(
      List<String> teams, String categoryId) {

    List<AssetManagement> assetsData =
        teams.stream()
            .map((String team) -> findAssetMetaData(categoryId, team))
            .filter(Objects::nonNull)
            .toList();

    if (assetsData.size() == TEAM_SIZE) {
      return assetsData;
    }
    return Collections.emptyList();
  }

  public void clearLastGenerationTeams() {
    lastGenerationTeams.clear();
  }
}
