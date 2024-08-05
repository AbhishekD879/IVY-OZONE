package com.oxygen.health.api;

import static org.junit.Assert.*;

import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;

public class AbstractPublisherHealthIndicatorTest {

  AbstractPublisherHealthIndicator testedEntity;

  @Before
  public void init() {
    testedEntity =
        new AbstractPublisherHealthIndicator() {

          @Override
          protected void doHealthCheck(Health.Builder builder) throws Exception {}

          @Override
          public List<Class<? extends ReloadableService>> getServicesToCheck() {
            return null;
          }

          @Override
          public AbstractServiceRegistry getServiceRegistry() {
            return null;
          }
        };
  }

  @Test
  public void summarizeByStatusDownToDown() {
    Health.Builder builder = new Health.Builder(Status.DOWN);

    testedEntity.summarize(builder, Status.UP);
    assertEquals(builder.build().getStatus(), Status.DOWN);

    testedEntity.summarize(builder, Status.DOWN);
    assertEquals(builder.build().getStatus(), Status.DOWN);

    testedEntity.summarize(builder, true);
    assertEquals(builder.build().getStatus(), Status.DOWN);

    testedEntity.summarize(builder, false);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void summarizeByStatusUpToDown() {
    Health.Builder builder = new Health.Builder(Status.UP);

    testedEntity.summarize(builder, Status.UP);
    assertEquals(builder.build().getStatus(), Status.UP);

    testedEntity.summarize(builder, Status.DOWN);
    assertEquals(builder.build().getStatus(), Status.DOWN);

    builder = new Health.Builder(Status.UP);

    testedEntity.summarize(builder, true);
    assertEquals(builder.build().getStatus(), Status.UP);

    testedEntity.summarize(builder, false);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }

  @Test
  public void summarizeByStatusUpToUp() {
    Health.Builder builder = new Health.Builder(Status.UP);

    testedEntity.summarize(builder, Status.UP);
    assertEquals(builder.build().getStatus(), Status.UP);

    testedEntity.summarize(builder, true);
    assertEquals(builder.build().getStatus(), Status.UP);
  }

  @Test
  public void summarizeNPLCheck() {
    Health.Builder builder = new Health.Builder(Status.UP);

    testedEntity.summarize(builder, null);
    assertEquals(builder.build().getStatus(), Status.DOWN);

    testedEntity.summarize(builder, Status.UP);
    assertEquals(builder.build().getStatus(), Status.DOWN);
  }
}
