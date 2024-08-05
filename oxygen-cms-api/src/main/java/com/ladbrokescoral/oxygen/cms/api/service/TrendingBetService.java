package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingBetRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class TrendingBetService extends AbstractService<TrendingBet> {

  private final TrendingBetRepository trendingBetRepository;
  private final List<String> types;

  public TrendingBetService(
      TrendingBetRepository trendingBetRepository,
      @Value("${trending-bets.type}") List<String> types) {
    super(trendingBetRepository);
    this.types = types;
    this.trendingBetRepository = trendingBetRepository;
  }

  public void validateType(String type) {
    if (!types.contains(type))
      throw new ValidationException(
          "Invalid type: '" + type + "', type should be either 'bet-slip' or 'bet-receipt'");
  }

  @Override
  public TrendingBet save(TrendingBet trendingBet) {
    validateType(trendingBet.getType());
    if (trendingBet.getId() != null) {
      trendingBetRepository
          .findById(trendingBet.getId())
          .ifPresent(trendingBet1 -> trendingBet.setType(trendingBet1.getType()));
    } else {
      checkIfEntityWithTypeAlreadyExists(trendingBet.getBrand(), trendingBet.getType());
    }
    return trendingBetRepository.save(trendingBet);
  }

  public void checkIfEntityWithTypeAlreadyExists(String brand, String type) {
    Optional<TrendingBet> trendingBet =
        trendingBetRepository.findTrendingBetByBrandAndType(brand, type);
    if (trendingBet.isPresent()) {
      throw new ValidationException("Trending bet with type '" + type + "' already exists");
    }
  }

  public Optional<TrendingBet> getTrendingBetsByBrand(String brand, String type) {
    validateType(type);
    return trendingBetRepository.findTrendingBetByBrandAndType(brand, type);
  }
}
