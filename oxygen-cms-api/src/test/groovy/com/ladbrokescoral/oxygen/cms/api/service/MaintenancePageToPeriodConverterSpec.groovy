package com.ladbrokescoral.oxygen.cms.api.service

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage

import java.time.Duration
import java.time.Instant

import spock.lang.Specification

class MaintenancePageToPeriodConverterSpec extends Specification {


  public static final String BRAND = "brand"

  def "convert to period with empty pages"() {
    when:
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Collections.emptyList())

    then:
    resultedPeriods.isEmpty()
  }

  def "convert to period with desktop and mobile"() {
    when:
    def startDate = Instant.now()
    def endDate = startDate.plus(Duration.ofHours(1))

    MaintenancePage page = createPage(startDate, endDate, true, true, true)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Collections.singletonList(page))

    then:
    resultedPeriods.size() == 1
    resultedPeriods[0].getBrand() == page.getBrand()
    resultedPeriods[0].getStart() == startDate.toEpochMilli()
    resultedPeriods[0].getEnd() == endDate.toEpochMilli()
  }

  def "convert to period with desktop and mobile overlap"() {
    //to cover case
    //-------desktop-------
    //   -------mobile---------
    when:
    def startDate1 = Instant.now()
    def endDate1 = startDate1.plus(Duration.ofMinutes(20))

    def startDate2 = Instant.now().plus(Duration.ofMinutes(10))
    def endDate2 = startDate2.plus(Duration.ofHours(1))

    MaintenancePage page1 = createPage(startDate1, endDate1, true,false,false)
    MaintenancePage page2 = createPage(startDate2, endDate2, false, true, true)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Arrays.asList(page1, page2))

    then:
    resultedPeriods.size() == 1
    resultedPeriods[0].getBrand() == page1.getBrand()
    resultedPeriods[0].getStart() == startDate2.toEpochMilli()
    resultedPeriods[0].getEnd() == endDate1.toEpochMilli()
  }

  def "convert to period with desktop and mobile overlap 2"() {
    //to cover case
    //-------desktop-------
    //   -------mobile---------
    //     ----desktop + mobile---
    //        -------desktop---------
    when:
    def now = Instant.now()
    def tenMinutes = Duration.ofMinutes(10)
    MaintenancePage page1 = createPage(now, now.plus(tenMinutes.multipliedBy(6)), true,false,false)
    MaintenancePage page2 = createPage(now.plus(tenMinutes),  now.plus(tenMinutes.multipliedBy(7)), false, true, false)
    MaintenancePage page3 = createPage(now.plus(tenMinutes.multipliedBy(2)), now.plus(tenMinutes.multipliedBy(8)), true, true, true)
    MaintenancePage page4 = createPage(now.plus(tenMinutes.multipliedBy(3)), now.plus(tenMinutes.multipliedBy(9)), true, false, false)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Arrays.asList(page1, page2, page3, page4))

    then:
    resultedPeriods.size() == 1
    resultedPeriods[0].getBrand() == page1.getBrand()
    resultedPeriods[0].getStart() == page2.getValidityPeriodStart().toEpochMilli()
    resultedPeriods[0].getEnd() == page3.getValidityPeriodEnd().toEpochMilli()
  }

  def "convert to period with desktop and mobile overlap 3"() {
    //to cover case
    //-------mobile---------
    //     -------desktop-------
    //                           ----desktop + mobile---
    //                             -------desktop---------
    when:
    def now = Instant.now()
    def tenMinutes = Duration.ofMinutes(10)
    MaintenancePage page1 = createPage(now, now.plus(tenMinutes.multipliedBy(6)), false,true,false)
    MaintenancePage page2 = createPage(now.plus(tenMinutes), now.plus(tenMinutes.multipliedBy(7)), true, false, false)
    MaintenancePage page3 = createPage(now.plus(tenMinutes.multipliedBy(8)), now.plus(tenMinutes.multipliedBy(12)), true, true, true)
    MaintenancePage page4 = createPage(now.plus(tenMinutes.multipliedBy(10)), now.plus(tenMinutes.multipliedBy(15)), true, false, false)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Arrays.asList(page1, page2, page3, page4))

    //copy to list as set doesn't guarantee order of resulted periods
    resultedPeriods = new ArrayList<>(resultedPeriods)
    resultedPeriods.sort(Comparator.comparing({m -> m.getStart()}))

    then:
    resultedPeriods.size() == 2
    resultedPeriods[0].getBrand() == page1.getBrand()
    resultedPeriods[0].getStart() == page2.getValidityPeriodStart().toEpochMilli()
    resultedPeriods[0].getEnd() == page1.getValidityPeriodEnd().toEpochMilli()

    resultedPeriods[1].getStart() == page3.getValidityPeriodStart().toEpochMilli()
    resultedPeriods[1].getEnd() == page3.getValidityPeriodEnd().toEpochMilli()
  }

  def "convert to period with desktop and mobile same time frame"() {
    //to cover case
    //-------desktop-------
    //-------tablet--------
    when:
    def now = Instant.now()
    def tenMinutes = Duration.ofMinutes(10)
    MaintenancePage page1 = createPage(now, now.plus(tenMinutes), true, false, false)
    MaintenancePage page2 = createPage(now, now.plus(tenMinutes), false, false, true)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Arrays.asList(page1, page2))

    then:
    resultedPeriods.size() == 1
    resultedPeriods[0].getBrand() == page1.getBrand()
    resultedPeriods[0].getStart() == page1.getValidityPeriodStart().toEpochMilli()
    resultedPeriods[0].getEnd() == page1.getValidityPeriodEnd().toEpochMilli()
  }

  def "convert to period with desktop and mobile not overlap"() {
    //to cover case
    //-------desktop-------
    //                     -------mobile---------
    when:
    def startDate1 = Instant.now()
    def endDate1 = startDate1.plus(Duration.ofMinutes(20))

    def startDate2 = endDate1
    def endDate2 = startDate2.plus(Duration.ofHours(1))

    MaintenancePage page1 = createPage(startDate1, endDate1, true,false, false)
    MaintenancePage page2 = createPage(startDate2, endDate2, false, true, false)
    def resultedPeriods = MaintenancePageToPeriodConverter.convertToMaintenancePeriods(BRAND, Arrays.asList(page1, page2))

    then:
    resultedPeriods.isEmpty()
  }

  MaintenancePage createPage(Instant startDate, Instant endDate, boolean desktop, boolean mobile, boolean tablet) {
    MaintenancePage maintenancePage = new MaintenancePage()
    maintenancePage.setId(UUID.randomUUID().toString())
    maintenancePage.setBrand(BRAND)
    maintenancePage.setValidityPeriodStart(startDate)
    maintenancePage.setValidityPeriodEnd(endDate)
    maintenancePage.setDesktop(desktop)
    maintenancePage.setMobile(mobile)
    maintenancePage.setTablet(tablet)
    return maintenancePage
  }
}
