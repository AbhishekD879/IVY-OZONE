package com.coral.oxygen.middleware.common.mappers;

import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.test.mock.mockito.MockBean;

public class SimpleMarketMapperTest {

  private static final String MKTFLAG_BB = "MKTFLAG_BB";
  private static final String EVFLAG_BB = "EVFLAG_BB";

  private static final String EXT_IDS = "BWIN_PG,-2095477391,";

  @MockBean private SimpleMarketMapper marketMapper;

  @Before
  public void init() {
    marketMapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
  }

  @Test
  public void mapEmpty() {
    SimpleMarketMapper mapper = new SimpleMarketMapper(new SimpleOutcomeMapper());
    Event d = new Event();
    mapper.map(d, new Market());
    Assert.assertNull(d.getAwayTeamExtIds());
  }

  @Test
  public void testMarketMapperForBYB() {
    Event d = new Event();
    d.setDrilldownTagNames(EVFLAG_BB);
    Market m = new Market();
    m.setDrilldownTagNames(MKTFLAG_BB);
    m.setExtIds(EXT_IDS);
    marketMapper.map(d, m);
    Assert.assertNotNull(d.getDrilldownTagNames());
  }

  @Test
  public void testMarketMapperForBYBNullExtIds() {
    Event d = new Event();
    d.setDrilldownTagNames(EVFLAG_BB);
    Market m = new Market();
    m.setDrilldownTagNames(MKTFLAG_BB);
    marketMapper.map(d, m);
    Assert.assertNotNull(d.getDrilldownTagNames());
  }

  @Test
  public void testMarketMapperForBYBNullExtIds1() {
    Event d = new Event();
    d.setDrilldownTagNames("EVFLAG_BL");
    Market m = new Market();
    m.setDrilldownTagNames(MKTFLAG_BB);
    m.setExtIds(EXT_IDS);
    marketMapper.map(d, m);
    Assert.assertNotNull(d.getDrilldownTagNames());
  }

  @Test
  public void testMarketMapperForBYBNullTags() {
    Event d = new Event();
    d.setDrilldownTagNames(EVFLAG_BB);
    Market m = new Market();
    m.setDrilldownTagNames("MKTFLAG_BL");
    m.setExtIds(EXT_IDS);
    marketMapper.map(d, m);
    Assert.assertNotNull(d.getDrilldownTagNames());
  }

  @Test
  public void testMarketMapperForBYBNullDrillDown() {
    Event d = new Event();
    d.setDrilldownTagNames(EVFLAG_BB);
    Market m = new Market();
    m.setExtIds(EXT_IDS);
    marketMapper.map(d, m);
    Assert.assertNotNull(m.getExtIds());
  }

  @Test
  public void testMarketMapperForBYBNull() {
    Event d = new Event();
    Market m = new Market();
    m.setDrilldownTagNames("MKTFLAG_BB");
    m.setExtIds(EXT_IDS);
    marketMapper.map(d, m);
    Assert.assertNotNull(m.getDrilldownTagNames());
  }
}
