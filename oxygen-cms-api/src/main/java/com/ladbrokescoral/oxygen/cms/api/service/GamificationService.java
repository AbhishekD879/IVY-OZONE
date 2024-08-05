package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonTeamDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.exception.GameCreationException;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class GamificationService extends AbstractService<Gamification> {

  private final GamificationRepository gamificationRepository;
  private final AssetManagementRepository assetManagementRepository;

  private ModelMapper modelMapper;

  private final SeasonService seasonService;

  public GamificationService(
      GamificationRepository gamificationRepository,
      AssetManagementRepository assetManagementRepository,
      ModelMapper modelMapper,
      SeasonService seasonService) {
    super(gamificationRepository);
    this.gamificationRepository = gamificationRepository;
    this.assetManagementRepository = assetManagementRepository;
    this.modelMapper = modelMapper;
    this.seasonService = seasonService;
  }

  public Optional<GamificationDetailsDto> getGamificationDetailsById(Gamification gamification) {
    Optional<Gamification> optionalGamification = Optional.ofNullable(gamification);
    Set<String> assetIds =
        getAssetManagementObjIds(
            optionalGamification.map(Arrays::asList).orElseGet(ArrayList::new));
    Map<String, AssetManagement> assetsManagementDetails =
        assetManagementRepository.findByIdIn(new ArrayList<>(assetIds)).stream()
            .collect(Collectors.toMap(AbstractEntity::getId, assetManagement -> assetManagement));

    return optionalGamification
        .map(e -> modelMapper.map(e, GamificationDetailsDto.class))
        .map(
            (GamificationDetailsDto gamificationDetailsDto) -> {
              gamificationDetailsDto
                  .getTeams()
                  .forEach(
                      (SeasonTeamDto seasonTeamDto) ->
                          mappedTeamAndSvgName(assetsManagementDetails, seasonTeamDto));
              return gamificationDetailsDto;
            });
  }

  public List<GamificationDto> findGamificationByBrand(String brand) {
    List<Season> seasonList = seasonService.findByBrand(brand);
    Map<String, Season> seasonMap =
        seasonList.stream().collect(Collectors.toMap(AbstractEntity::getId, season -> season));
    List<Gamification> gamificationList = gamificationRepository.findByBrand(brand);
    Set<String> assetIds = getAssetManagementObjIds(gamificationList);
    Map<String, AssetManagement> assetManagementDetails =
        assetManagementRepository.findByIdIn(new ArrayList<>(assetIds)).stream()
            .collect(Collectors.toMap(AbstractEntity::getId, assetManagement -> assetManagement));

    return gamificationList.stream()
        .map(e -> modelMapper.map(e, GamificationDto.class))
        .map(
            (GamificationDto gamificationDto) -> {
              if (seasonMap.containsKey(gamificationDto.getSeasonId())) {
                Season season = seasonMap.get(gamificationDto.getSeasonId());
                gamificationDto.setSeasonName(season.getSeasonName());
                gamificationDto.setDisplayFrom(season.getDisplayFrom());
                gamificationDto.setDisplayTo(season.getDisplayTo());
              }
              return gamificationDto;
            })
        .map(
            (GamificationDto gamificationDto) -> {
              gamificationDto
                  .getTeams()
                  .forEach(sTeam -> mappedTeamAndSvgName(assetManagementDetails, sTeam));
              return gamificationDto;
            })
        .collect(Collectors.toList());
  }

  private Set<String> getAssetManagementObjIds(List<Gamification> gamificationList) {
    return gamificationList.stream()
        .flatMap(
            gam ->
                gam.getTeams().stream()
                    .map(SeasonTeam::getAssetManagementObjectId)
                    .collect(Collectors.toList())
                    .stream())
        .collect(Collectors.toSet());
  }

  private void mappedTeamAndSvgName(
      Map<String, AssetManagement> assetManagementDetails, SeasonTeamDto sTeam) {
    AssetManagement assetManagement =
        assetManagementDetails.get(sTeam.getAssetManagementObjectId());
    if (Objects.nonNull(assetManagement)) {
      sTeam.setDisplayName(assetManagement.getTeamName());
      sTeam.setSvg(
          Objects.nonNull(assetManagement.getTeamsImage())
              ? assetManagement.getTeamsImage().getSvg()
              : "");
    }
  }

  public Optional<Gamification> findGamificationBySeasonId(String seasonId) {
    return gamificationRepository.findBySeasonId(seasonId);
  }

  public List<Optional<Gamification>> findAllGamificationBySeasonId(List<String> seasonIds) {
    return gamificationRepository.findBySeasonIdIn(seasonIds);
  }

  public void validateGameTeamNameWithSeasonTeamName(Game game) {
    if (!validateIsTeamNameNull(game)) {
      log.error("isNonPLTeam field is null");
      throw new GameCreationException("isNonPLTeam field is null");
    }
    Set<String> gameTeamsName = new HashSet<>();
    game.getEvents()
        .forEach(
            (GameEvent gameEvent) -> {
              if (Boolean.FALSE.equals(gameEvent.getHome().getIsNonPLTeam())) {
                gameTeamsName.add(gameEvent.getHome().getDisplayName());
              }
              if (Boolean.FALSE.equals(gameEvent.getAway().getIsNonPLTeam())) {
                gameTeamsName.add(gameEvent.getAway().getDisplayName());
              }
            });

    Optional<Gamification> gamificationOptional =
        gamificationRepository.findBySeasonId(game.getSeasonId());

    if (gamificationOptional.isPresent()) {
      List<String> assetIds =
          gamificationOptional.get().getTeams().stream()
              .map(SeasonTeam::getAssetManagementObjectId)
              .collect(Collectors.toList());

      Stream<AssetManagement> assetManagementSteam =
          StreamSupport.stream(assetManagementRepository.findAllById(assetIds).spliterator(), true);

      final List<String> assetTeamsName =
          assetManagementSteam
              .map(as -> as.getTeamName().toUpperCase())
              .collect(Collectors.toList());

      List<String> notMatchTeam =
          gameTeamsName.stream()
              .filter(tName -> !assetTeamsName.contains(tName.toUpperCase()))
              .collect(Collectors.toList());

      if (!notMatchTeam.isEmpty()) {
        log.error("Game Team Names does not match with Season Team Names : {}", notMatchTeam);
        throw new GameCreationException("teamMisMatch:" + notMatchTeam);
      }
    } else {
      log.error("gamificationNotExist:Gamification does not exist");
      throw new GameCreationException("gamificationNotExist:Gamification does not exist");
    }
  }

  private boolean validateIsTeamNameNull(Game game) {
    boolean flag = true;
    for (GameEvent ge : game.getEvents()) {
      if (Objects.isNull(ge.getHome().getIsNonPLTeam())
          || Objects.isNull(ge.getAway().getIsNonPLTeam())) {
        flag = false;
        break;
      }
    }
    return flag;
  }
}
