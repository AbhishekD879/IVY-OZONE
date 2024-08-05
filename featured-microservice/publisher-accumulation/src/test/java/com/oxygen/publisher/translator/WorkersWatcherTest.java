package com.oxygen.publisher.translator;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.Assert.assertEquals;
import static org.mockito.BDDMockito.given;
import static org.mockito.BDDMockito.then;
import static org.mockito.Mockito.times;

import com.oxygen.publisher.api.EntityLock;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class WorkersWatcherTest {

  public static final String chainId = "TEST_CHAIN";

  private static final Object testModel = new Object();

  @Mock private EntityLock locker;

  private WorkersWatcher watcher;
  private AbstractWorker<Object, Object> rootWorker;

  @Before
  public void init() {
    given(locker.getEntityGUID()).willReturn(chainId);

    watcher = new WorkersWatcher(chainId);
  }

  private AbstractWorker<Object, Object> createAbstractWorker(String chainId, final int loopCount) {
    return new AbstractWorker<Object, Object>(locker) {
      @Override
      public void onProcess(Object model) {
        assertThat(model).isEqualTo(testModel);
        if (loopCount > 0) {
          assertThat(isWorking()).isTrue();
          this.accept(
              model,
              () -> {
                AbstractWorker<Object, Object> nextWorker =
                    createAbstractWorker("Step" + loopCount, loopCount - 1);
                watcher.add(nextWorker);
                return nextWorker;
              });
          assertThat(isWorking()).isTrue();
        }
      }
    };
  }

  /**
   * Chain life-cycle test. Test condition means that RootWorker is active until the last step of
   * the chain has been executed.
   */
  @Test
  public void testIsAliveOnWatcherByRootTask_OK() {
    rootWorker = createAbstractWorker("Step", 3);
    watcher.add(rootWorker);

    then(locker).should(times(1)).getEntityGUID();

    assertThat(watcher.isAlive()).isTrue();
    rootWorker.start(testModel);
    assertThat(watcher.isAlive()).isFalse();
    assertEquals(
        3,
        watcher.getFollowers().stream()
            .filter(weakRef -> weakRef.get() != null)
            .filter(weakRef -> weakRef.get().isWorking())
            .count());
    assertEquals(
        1,
        watcher.getFollowers().stream()
            .filter(weakRef -> weakRef.get() != null)
            .filter(weakRef -> !weakRef.get().isWorking())
            .count());
  }

  /**
   * Chain life-cycle test. Test condition means that RootWorker is active in spite of it was
   * interrupted by finalize method. This case
   */
  @Test
  public void testFinalize_OK() {
    rootWorker =
        new AbstractWorker<Object, Object>(locker) {
          @Override
          protected void onProcess(Object model) {
            assertThat(model).isNull();
            assertThat(isWorking()).isTrue();
          }
        };
    watcher.add(rootWorker);

    then(locker).should(times(1)).getEntityGUID();

    assertThat(watcher.isAlive()).isTrue();
    rootWorker.finalizeWork();
    assertThat(watcher.isAlive()).isTrue();
  }
}
