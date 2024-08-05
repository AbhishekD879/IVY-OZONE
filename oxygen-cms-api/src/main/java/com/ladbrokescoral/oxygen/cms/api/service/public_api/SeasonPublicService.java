package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationService;
import com.ladbrokescoral.oxygen.cms.api.service.SeasonService;
import java.util.*;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.modelmapper.TypeToken;
import org.springframework.stereotype.Service;

@Service
public class SeasonPublicService {
  private final SeasonService seasonService;
  private final GamificationService gamificationService;
  private final AssetManagementRepository assetManagementRepository;

  private ModelMapper modelMapper;

  public SeasonPublicService(
      SeasonService seasonService,
      ModelMapper modelMapper,
      GamificationService gamificationService,
      AssetManagementRepository assetManagementRepository) {
    this.seasonService = seasonService;
    this.modelMapper = modelMapper;
    this.gamificationService = gamificationService;
    this.assetManagementRepository = assetManagementRepository;
  }

  public List<SeasonDto> findAllByBrand(String brand) {
    return seasonService.findByBrand(brand).stream()
        .map(e -> modelMapper.map(e, SeasonDto.class))
        .collect(Collectors.toList());
  }

  public Optional<SeasonCacheDto> getActiveSeason(String brand) {
    Optional<Season> activeSeason = seasonService.getActiveSeason(brand).stream().findAny();
    if (activeSeason.isPresent()) {
      Optional<SeasonCacheDto> seasonCacheDto =
          activeSeason.map(e -> modelMapper.map(e, SeasonCacheDto.class));
      Optional<Gamification> gamification =
          gamificationService.findGamificationBySeasonId(activeSeason.get().getId());
      return gamification
          .map(
              gm ->
                  seasonCacheDto.map(
                      (SeasonCacheDto sDto) -> {
                        sDto.setTeams(getTeamList(gm));
                        sDto.setBadgeTypes(
                            modelMapper.map(
                                gm.getBadgeTypes(),
                                new TypeToken<List<BadgeTypeCacheDto>>() {}.getType()));
                        return sDto;
                      }))
          .orElse(seasonCacheDto);
    }
    return Optional.empty();
  }

  public List<SeasonGamificationDto> getCurrentFutureSeasons(String brand) {
    Map<String, Season> seasonMap =
        seasonService.getCurrentFutureSeasons(brand).stream()
            .collect(Collectors.toMap(AbstractEntity::getId, season -> season));

    Map<String, List<SeasonTeamDto>> gamificationMap =
        gamificationService.findAllGamificationBySeasonId(new ArrayList<>(seasonMap.keySet()))
            .stream()
            .map(Optional::get)
            .collect(
                Collectors.toMap(
                    Gamification::getSeasonId, gm -> getSeasonTeamPublicDtoList(gm.getTeams())));

    return seasonMap.values().stream()
        .map(season -> modelMapper.map(season, SeasonGamificationDto.class))
        .map(
            (SeasonGamificationDto sGamificationDto) -> {
              if (gamificationMap.containsKey(sGamificationDto.getId())) {
                sGamificationDto.setTeams(gamificationMap.get(sGamificationDto.getId()));
              }
              return sGamificationDto;
            })
        .collect(Collectors.toList());
  }

  public List<SeasonCacheDto> getCurrentFutureSeasonDetails(String brand) {
    Map<String, Season> seasonMap =
        seasonService.getCurrentFutureSeasons(brand).stream()
            .filter(season -> season.getDisplayTo().toEpochMilli() > System.currentTimeMillis())
            .collect(Collectors.toMap(AbstractEntity::getId, season -> season));
    List<Optional<Gamification>> gamification =
        gamificationService.findAllGamificationBySeasonId(new ArrayList<>(seasonMap.keySet()));
    return seasonMap.values().stream()
        .map(
            (Season season) -> {
              SeasonCacheDto seasonCacheDto = modelMapper.map(season, SeasonCacheDto.class);
              Optional<Gamification> gamificationOptional =
                  gamification.stream()
                      .map(Optional::get)
                      .filter(gm -> gm.getSeasonId().equals(seasonCacheDto.getId()))
                      .findFirst();
              gamificationOptional.ifPresent(
                  (Gamification g) -> {
                    seasonCacheDto.setTeams(
                        modelMapper.map(
                            getSeasonTeamPublicDtoList(g.getTeams()),
                            new TypeToken<List<TeamCacheDto>>() {}.getType()));
                    seasonCacheDto.setBadgeTypes(
                        modelMapper.map(
                            g.getBadgeTypes(),
                            new TypeToken<List<BadgeTypeCacheDto>>() {}.getType()));
                  });
              return seasonCacheDto;
            })
        .collect(Collectors.toList());
  }

  private List<TeamCacheDto> getTeamList(Gamification gamification) {
    List<String> amIDs =
        gamification.getTeams().stream()
            .map(SeasonTeam::getAssetManagementObjectId)
            .collect(Collectors.toList());
    return assetManagementRepository.findByIdIn(amIDs).stream()
        .map(e -> new TeamCacheDto(e.getTeamName()))
        .collect(Collectors.toList());
  }

  private List<SeasonTeamDto> getSeasonTeamPublicDtoList(List<SeasonTeam> seasonTeamList) {
    List<String> amIDs =
        seasonTeamList.stream()
            .map(SeasonTeam::getAssetManagementObjectId)
            .collect(Collectors.toList());
    return assetManagementRepository.findByIdIn(amIDs).stream()
        .map(
            (AssetManagement e) -> {
              SeasonTeamDto sTeamDto = new SeasonTeamDto();
              sTeamDto.setDisplayName(e.getTeamName());
              sTeamDto.setAssetManagementObjectId(e.getId());
              sTeamDto.setSvg(Objects.nonNull(e.getTeamsImage()) ? e.getTeamsImage().getSvg() : "");
              sTeamDto.setPath(
                  Objects.nonNull(e.getTeamsImage()) ? e.getTeamsImage().getPath() : "");
              sTeamDto.setFileName(
                  Objects.nonNull(e.getTeamsImage()) ? e.getTeamsImage().getFilename() : "");
              return sTeamDto;
            })
        .collect(Collectors.toList());
  }
}
