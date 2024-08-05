package com.oxygen.publisher.translator

import com.oxygen.publisher.api.EntityLock
import spock.lang.Ignore
import spock.lang.Specification

import java.util.function.Consumer

class DiagnosticServiceSpec extends Specification {
  DiagnosticService diagnosticService
  String workersGuid = "test"

  def diagnostic = Mock(Consumer)
  def locker = Mock(EntityLock)


  def setup() {
    diagnosticService = new DiagnosticService(0)
    diagnosticService.setDiagnosticListener { message ->
      assert message != null
      assert message != ""
    }
  }

  def "On Problem Detection_Has Some"() throws Exception {
    when:
    AbstractWorker worker = createAbstractWorker()
    WorkersWatcher watcher = diagnosticService.toDiagnostic(worker)
    //prevent for destroy worker by GC
    watcher.add(worker)
    diagnosticService.start()
    Thread.sleep(500)

    then:
    locker.getEntityGUID() >> workersGuid
    diagnosticService.getWatchers().size() == 1
  }

  private AbstractWorker createAbstractWorker() {
    return new AbstractWorker<Object, Object>(locker) {
          @Override
          void onProcess(Object model) {
            assert isWorking() == true
            assert model == null
          }
        };
  }

  /**
   * This case means what the first worker is neither run and never stop.
   */
  def "On Problem Detection_Concurrent Access"() throws InterruptedException {
    when:
    AbstractWorker firstWorker = createAbstractWorker()

    diagnosticService.setDiagnosticListener(diagnostic)
    diagnosticService.toDiagnostic(firstWorker)
    diagnosticService.start()

    for (int i = 0; i < 30; i++) {
      AbstractWorker worker = createAbstractWorker()
      diagnosticService.toDiagnostic(worker)
      worker.start()
    }

    then:
    locker.getEntityGUID() >> workersGuid
    diagnosticService.getWatchers().find { entity -> entity.value.isAlive() }.findAll().size() == 1
  }

  /**
   * Test Case is means working chains were finished successfully.
   */
  def "On Problem Detection_Empty Run"() throws InterruptedException {
    when:
    diagnosticService.start()
    for (int i = 0; i < 10; i++) {
      AbstractWorker<?, ?> worker = createAbstractWorker()
      diagnosticService.toDiagnostic(worker)
      worker.start()
    }

    then:
    locker.getEntityGUID() >> workersGuid
    diagnosticService.getWatchers().find { entity -> entity.value.isAlive() } == null
  }

  def "Test States Of Diag Service_Empty Running"() throws InterruptedException {
    when:
    diagnosticService.start()
    Thread.sleep(10)

    then:
    diagnosticService.isAlive()
  }

  def "Test States Of Diag Service_Empty Stopped"() throws InterruptedException {
    when:
    diagnosticService.start()
    Thread.sleep(10)

    diagnosticService.setKeepRunning(false)
    boolean isAlive = diagnosticService.isAlive()
    int count = 0
    while (isAlive && count < 500) {
      Thread.sleep(1)
      isAlive = diagnosticService.isAlive()
    }

    then:
    !diagnosticService.isAlive()
  }
}
