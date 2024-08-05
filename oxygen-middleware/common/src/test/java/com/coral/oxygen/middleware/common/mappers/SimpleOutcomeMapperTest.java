package com.coral.oxygen.middleware.common.mappers;

import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.model.*;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {SimpleOutcomeMapper.class})
@AutoConfigureMockMvc(addFilters = false)
@MockitoSettings(strictness = Strictness.LENIENT)
public class SimpleOutcomeMapperTest {

  @MockBean private SimpleOutcomeMapper simpleOutcomeMapper;
  @Mock private Outcome outcome;

  @Before
  public void init() {
    simpleOutcomeMapper = new SimpleOutcomeMapper();
  }

  @Test
  public void mapEmpty() {
    Event d = new Event();
    Price p = new Price();
    p.setId("1");
    p.setIsActive(Boolean.TRUE);
    Price p1 = new Price();
    p1.setId("2");
    p1.setIsActive(Boolean.FALSE);
    List<Price> priceList = new ArrayList<>();
    priceList.add(p);
    priceList.add(p1);
    Children child = new Children();
    child.setPrice(p);
    Children child1 = new Children();
    child1.setPrice(p1);
    List<Children> childrenList = new ArrayList<>();
    childrenList.add(child);
    childrenList.add(child1);
    outcome.setChildren(childrenList);
    when(outcome.getPrices()).thenReturn(priceList);
    simpleOutcomeMapper.map(d, new Market(), outcome);
    verify(outcome, times(3)).getPrices();
  }

  @Test
  public void testOutcomeMapperForBYB() {
    Event d = new Event();
    Price p = new Price();
    p.setId("1");
    p.setIsActive(Boolean.TRUE);
    Price p1 = new Price();
    p1.setId("2");
    p1.setIsActive(Boolean.FALSE);
    List<Price> priceList = new ArrayList<>();
    priceList.add(p);
    priceList.add(p1);
    Children child = new Children();
    child.setPrice(p);
    Children child1 = new Children();
    child1.setPrice(p1);
    List<Children> childrenList = new ArrayList<>();
    childrenList.add(child);
    childrenList.add(child1);
    outcome.setChildren(childrenList);
    when(outcome.getPrices()).thenReturn(priceList);
    when(outcome.getExtIds()).thenReturn("BWIN_PG,-2095477391,");
    simpleOutcomeMapper.map(d, new Market(), outcome);
    verify(outcome, times(3)).getPrices();
  }
}
