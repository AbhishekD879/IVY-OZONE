package com.ladbrokescoral.oxygen.cms.api.service;

import static java.lang.Long.max;
import static java.lang.Long.min;
import static org.apache.commons.lang3.BooleanUtils.isTrue;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.experimental.UtilityClass;

@UtilityClass
public class MaintenancePageToPeriodConverter {

  private static final Comparator<MaintenancePage> START_DATE_COMPARATOR =
      Comparator.comparing(MaintenancePage::getValidityPeriodStart);

  public Set<BrandMaintenancePeriod> convertToMaintenancePeriods(
      String brand, List<MaintenancePage> maintenance) {
    List<MaintenancePage> desktopMaintenance =
        filterMaintenance(maintenance, p -> isTrue(p.getDesktop()));
    List<MaintenancePage> mobileMaintenance =
        filterMaintenance(maintenance, p -> isTrue(p.getMobile()) || isTrue(p.getTablet()));

    Set<BrandMaintenancePeriod> periods = new HashSet<>();
    int desktopIndx = 0;
    int mobileIndx = 0;
    BrandMaintenancePeriod lastPeriod = null;
    while (desktopIndx < desktopMaintenance.size() && mobileIndx < mobileMaintenance.size()) {
      MaintenancePage desktop = desktopMaintenance.get(desktopIndx);
      MaintenancePage mobile = mobileMaintenance.get(mobileIndx);
      if (desktop.getId().equals(mobile.getId()) || isOverlapping(desktop, mobile)) {
        BrandMaintenancePeriod newMaintenancePeriod =
            createMaintenancePeriod(brand, desktop, mobile);
        lastPeriod = mergePeriodsIfOverlapped(lastPeriod, newMaintenancePeriod);
        periods.add(lastPeriod);
      }

      if (desktop.getValidityPeriodStart().isBefore(mobile.getValidityPeriodStart())) {
        desktopIndx++;
      } else {
        mobileIndx++;
      }
    }
    return periods;
  }

  private BrandMaintenancePeriod mergePeriodsIfOverlapped(
      BrandMaintenancePeriod lastPeriod, BrandMaintenancePeriod newPeriod) {
    if (Objects.nonNull(lastPeriod) && isOverlapping(lastPeriod, newPeriod)) {
      lastPeriod.extend(newPeriod);
      return lastPeriod;
    }
    return newPeriod;
  }

  private List<MaintenancePage> filterMaintenance(
      List<MaintenancePage> maintenance, Predicate<MaintenancePage> pageFilter) {
    return maintenance.stream()
        .filter(pageFilter)
        .sorted(START_DATE_COMPARATOR)
        .collect(Collectors.toList());
  }

  private boolean isOverlapping(MaintenancePage page1, MaintenancePage page2) {
    return (!page1.getValidityPeriodStart().isAfter(page2.getValidityPeriodStart())
            && page2.getValidityPeriodStart().isBefore(page1.getValidityPeriodEnd()))
        || (!page2.getValidityPeriodStart().isAfter(page1.getValidityPeriodStart())
            && page1.getValidityPeriodStart().isBefore(page2.getValidityPeriodEnd()));
  }

  private boolean isOverlapping(BrandMaintenancePeriod period1, BrandMaintenancePeriod period2) {
    return (period2.getStart() >= period1.getStart() && period2.getStart() < period1.getEnd())
        || (period1.getStart() >= period2.getStart() && period1.getStart() < period2.getEnd());
  }

  private BrandMaintenancePeriod createMaintenancePeriod(
      String brand, MaintenancePage desktop, MaintenancePage mobile) {
    BrandMaintenancePeriod maintenancePeriod = new BrandMaintenancePeriod();
    maintenancePeriod.setBrand(brand);
    maintenancePeriod.setStart(
        max(
            desktop.getValidityPeriodStart().toEpochMilli(),
            mobile.getValidityPeriodStart().toEpochMilli()));
    maintenancePeriod.setEnd(
        min(
            desktop.getValidityPeriodEnd().toEpochMilli(),
            mobile.getValidityPeriodEnd().toEpochMilli()));
    return maintenancePeriod;
  }
}
