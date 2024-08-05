package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueLinkService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.data.mongodb.core.mapping.event.BeforeSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class LeagueLinksSaveListener extends BasicMongoEventListener<LeagueLink> {

  private static final String LINKS_PATH = "api/{0}/league-links";
  private final LeagueLinkService leagueLinkService;

  @Autowired
  public LeagueLinksSaveListener(
      @Qualifier("publicViewOnlyDelivery") DeliveryNetworkService context,
      LeagueLinkService leagueLinkService) {
    super(context);
    this.leagueLinkService = leagueLinkService;
  }

  @Override
  public void onBeforeSave(BeforeSaveEvent<LeagueLink> event) {
    LeagueLink oldLink = event.getSource();
    String linkId = oldLink.getId();
    String brand = oldLink.getBrand();

    if (linkId == null || linkId.trim().isEmpty()) {
      return;
    }

    Optional<LeagueLink> one = leagueLinkService.findOne(linkId);
    List<Integer> couponsThatWillBeRemoved =
        one.map(LeagueLink::getCouponIds).orElseGet(Collections::emptyList);
    couponsThatWillBeRemoved.removeAll(oldLink.getCouponIds());

    couponsThatWillBeRemoved.forEach(
        couponId ->
            uploadCollection(
                brand,
                LINKS_PATH,
                String.valueOf(couponId),
                getLeagueLinksForCouponsExcludeThoseThatWillBeDeleted(linkId, brand, couponId)));
  }

  private List<LeagueLink> getLeagueLinksForCouponsExcludeThoseThatWillBeDeleted(
      String linkId, String brand, Integer couponId) {
    return leagueLinkService.getEnabledLeagueLinksByCouponId(brand, couponId).stream()
        .filter(link -> !linkId.equals(link.getId()))
        .collect(Collectors.toList());
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LeagueLink> event) {
    LeagueLink savedLink = event.getSource();
    List<Integer> couponIds = savedLink.getCouponIds();
    String brand = savedLink.getBrand();

    couponIds.forEach(
        couponId ->
            uploadCollection(
                brand,
                LINKS_PATH,
                String.valueOf(couponId),
                leagueLinkService.getEnabledLeagueLinksByCouponId(brand, couponId)));
  }
}
