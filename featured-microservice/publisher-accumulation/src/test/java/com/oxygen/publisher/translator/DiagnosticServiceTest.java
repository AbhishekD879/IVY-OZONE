package com.oxygen.publisher.translator;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import com.oxygen.publisher.api.EntityLock;
import java.util.function.Consumer;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

/** Created by Aliaksei Yarotski on 1/9/18. */
@Ignore
@Deprecated
@RunWith(MockitoJUnitRunner.class)
public class DiagnosticServiceTest {

  private DiagnosticService diagnosticService;

  @Mock Consumer<String> diagnostic;

  @Mock EntityLock locker;

  @Before
  public void init() {
    this.diagnosticService = new DiagnosticService(0);
    diagnosticService.setDiagnosticListener(
        (message) -> {
          assertThat(message).isNotEmpty();
        });
  }

  @Test
  public void onProblemDetection_HasSome() throws Exception {
    AbstractWorker worker = createAbstractWorker();
    WorkersWatcher watcher = diagnosticService.toDiagnostic(worker);
    // prevent for destroy worker by GC
    watcher.add(worker);

    diagnosticService.start();
    Thread.sleep(500);
    assertThat(diagnosticService.getWatchers().size()).isEqualTo(1);
  }

  private AbstractWorker createAbstractWorker() {
    return new AbstractWorker<Object, Object>(locker) {
      @Override
      public void onProcess(Object model) {
        assertThat(model).isNull();
      }
    };
  }

  @Test
  public void onProblemDetection_concurrentAccess() throws InterruptedException {

    WorkersWatcher watcher = WorkersWatcher.createWatcher("#0");
    AbstractWorker<?, ?> worker = createAbstractWorker();
    watcher.add(worker);

    diagnosticService.setDiagnosticListener(diagnostic);
    diagnosticService.start();

    for (int i = 0; i < 30; i++) {
      diagnosticService.toDiagnostic(createAbstractWorker());
    }
    worker = null;
    System.gc();
    Thread.sleep(1000);
    assertThat(diagnosticService.getWatchers().size()).isEqualTo(0);
  }

  @Ignore // fails on bitbucket env. TODO fix and enable it back
  @Test
  public void onProblemDetection__emptyRun() throws InterruptedException {
    diagnosticService.start();

    for (int i = 0; i < 10; i++) {
      diagnosticService.toDiagnostic(createAbstractWorker());
    }
    Thread.sleep(1000);
    assertThat(diagnosticService.getWatchers().size()).isEqualTo(0);
  }

  @Test
  public void testStatesOfDiagService_emptyRun() throws InterruptedException {
    diagnosticService.start();
    Thread.sleep(10);
    assertThat(diagnosticService.isAlive()).isTrue();
    diagnosticService.setKeepRunning(false);
    boolean isAlive = diagnosticService.isAlive();
    int count = 0;
    while (isAlive && count < 500) {
      Thread.sleep(1);
      isAlive = diagnosticService.isAlive();
    }
    assertThat(diagnosticService.isAlive()).isFalse();
  }
}
