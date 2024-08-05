package com.coral.oxygen.edp.model.mapping;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import java.util.Collections;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class OutcomeCorrectPriceTypeMapperTest {

  private OutcomeCorrectPriceTypeMapper mapper;

  @Mock private OutcomeMapper chain;

  @Before
  public void setUp() {
    Mockito.when(chain.map(any(), any(), any())).thenReturn(new OutputOutcome());
    mapper = new OutcomeCorrectPriceTypeMapper(chain);
  }

  @Test
  public void testSpFalseLpFalsePricesNull() {
    // preparation
    Market market = new Market();

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return null;
          }
        };
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpFalseLpFalsePricesNotNull() {
    // preparation
    Market market = new Market();

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return Collections.singletonList(new Price());
          }
        };
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpTrueLpFalsePricesNotNull() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(true);

    Outcome outcome = new Outcome();

    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals("SP", outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpTrueLpFalsePricesNull() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(true);
    market.setIsLpAvailable(false);

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return null;
          }
        };
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals("SP", outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpTrueLpTruePricesNull() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(true);
    market.setIsLpAvailable(true);

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return null;
          }
        };
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals("SP", outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpTrueLpTruePricesNotNull() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(true);
    market.setIsLpAvailable(true);

    Outcome outcome = new Outcome();
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals("LP", outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpFalseLpTruePricesNotNull() {
    // preparation
    Market market = new Market();
    market.setIsLpAvailable(true);

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return Collections.singletonList(new Price());
          }
        };

    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals("LP", outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testSpFalseLpTruePricesNull() {
    // preparation
    Market market = new Market();
    market.setIsLpAvailable(true);

    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return null;
          }
        };

    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testLPWithNoPrices() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(false);
    market.setIsLpAvailable(true);
    Outcome outcome =
        new Outcome() {
          @Override
          public List<Price> getPrices() {
            return Collections.singletonList(new Price());
          }
        };
    outcome.setHasPriceStream(false);
    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getHasPriceStream());
  }

  @Test
  public void testNonLP() {
    // preparation
    Market market = new Market();
    market.setIsLpAvailable(false);

    Outcome outcome = new Outcome();

    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getCorrectPriceType());
  }

  @Test
  public void testNonLPWithprices() {
    // preparation
    Market market = new Market();
    market.setIsSpAvailable(false);
    market.setIsLpAvailable(false);

    Outcome outcome = new Outcome();

    // action
    OutputOutcome outputOutcome = mapper.map(null, market, outcome);

    // verification
    Assert.assertEquals(null, outputOutcome.getCorrectPriceType());
  }
}
