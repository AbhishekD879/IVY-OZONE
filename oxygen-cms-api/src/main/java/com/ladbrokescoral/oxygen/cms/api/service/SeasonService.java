package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.SeasonDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonUserDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.GameRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.GamificationRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SeasonRepository;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class SeasonService extends AbstractService<Season> {

  private final SeasonRepository seasonRepository;
  private final GamificationRepository gamificationRepository;
  private final GameRepository gameRepository;

  private ModelMapper modelMapper;

  public SeasonService(
      SeasonRepository seasonRepository,
      GamificationRepository gamificationRepository,
      GameRepository gameRepository,
      ModelMapper modelMapper) {
    super(seasonRepository);
    this.seasonRepository = seasonRepository;
    this.gamificationRepository = gamificationRepository;
    this.gameRepository = gameRepository;
    this.modelMapper = modelMapper;
  }

  public List<SeasonDetailsDto> findSeasonsByBrand(String brand, Sort sort) {
    List<Gamification> gamificationList = gamificationRepository.findByBrand(brand);
    List<Game> gameList = gameRepository.findByBrand(brand);
    return seasonRepository.findByBrand(brand, sort).stream()
        .map(e -> modelMapper.map(e, SeasonDetailsDto.class))
        .map(
            (SeasonDetailsDto seasonDetailsDto) -> {
              Optional<Gamification> gamificationOptional =
                  isGamificationLinked(gamificationList, seasonDetailsDto.getId());
              if (gamificationOptional.isPresent()) {
                seasonDetailsDto.setGamificationLinked(true);
              }
              List<String> games = isGameLinked(gameList, seasonDetailsDto.getId());
              if (!games.isEmpty()) {
                seasonDetailsDto.setGameLinked(true);
                seasonDetailsDto.setGamesLinked(games);
              }
              return seasonDetailsDto;
            })
        .collect(Collectors.toList());
  }

  public List<Season> getSeasonBetweenDates(Season season) {
    Instant fromDate =
        season.getDisplayFrom().plus(0, ChronoUnit.DAYS).truncatedTo(ChronoUnit.DAYS);
    Instant toDate = season.getDisplayTo().plus(1, ChronoUnit.DAYS).truncatedTo(ChronoUnit.DAYS);
    return seasonRepository.findByBrandAndDisplayToIsGreaterThanEqualAndDisplayFromIsLessThan(
        season.getBrand(), fromDate, toDate);
  }

  public List<Season> getActiveSeason(String brand) {
    return seasonRepository.findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
        brand, Instant.now(), Instant.now());
  }

  public List<Season> getCurrentFutureSeasons(String brand) {
    List<Season> activeSeasonList = getActiveSeason(brand);
    Instant fromDate = Instant.now().plus(0, ChronoUnit.DAYS).truncatedTo(ChronoUnit.DAYS);
    if (!activeSeasonList.isEmpty()) {
      fromDate =
          activeSeasonList
              .get(0)
              .getDisplayFrom()
              .plus(0, ChronoUnit.DAYS)
              .truncatedTo(ChronoUnit.DAYS);
    }
    return seasonRepository.findByBrandAndDisplayFromIsGreaterThanEqual(brand, fromDate);
  }

  public Optional<SeasonUserDetailsDto> getSeasonById(Optional<Season> season, String id) {
    if (season.isPresent()) {
      return season
          .map(e -> modelMapper.map(e, SeasonUserDetailsDto.class))
          .map(
              (SeasonUserDetailsDto sdDto) -> {
                if (gamificationRepository.findBySeasonId(id).isPresent()) {
                  sdDto.setGamificationLinked(true);
                }
                List<String> gamesList = isGameLinked(gameRepository.findBySeasonId(id), id);
                if (!gamesList.isEmpty()) {
                  sdDto.setGameLinked(true);
                  sdDto.setGamesLinked(gamesList);
                }
                return sdDto;
              });
    } else {
      throw new NotFoundException("Season Not present");
    }
  }

  private Optional<Gamification> isGamificationLinked(
      List<Gamification> gamificationList, String seasonId) {
    return gamificationList.stream()
        .filter(gamification -> seasonId.equals(gamification.getSeasonId()))
        .findFirst();
  }

  private List<String> isGameLinked(List<Game> gameList, String seasonId) {
    return gameList.stream()
        .filter(game -> seasonId.equals(game.getSeasonId()))
        .map(Game::getTitle)
        .collect(Collectors.toList());
  }
}
