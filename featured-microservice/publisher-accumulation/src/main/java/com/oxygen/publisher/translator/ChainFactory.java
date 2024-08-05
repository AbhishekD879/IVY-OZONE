package com.oxygen.publisher.translator;

import com.oxygen.publisher.api.EntityLock;
import java.util.UUID;
import java.util.function.BiConsumer;

/** Created by Aliaksei Yarotski on 2/5/18. */
public interface ChainFactory {

  AbstractWorker getScheduledJob();

  DiagnosticService diagnosticService();

  default <C, P> AbstractWorker<C, P> and(
      String entityGUID, BiConsumer<AbstractWorker<C, P>, C> onProcess) {
    AbstractWorker<C, P> thisWorker =
        new ChainAbstractWorker(entityGUID + UUID.randomUUID(), onProcess);
    toDiagnostic(thisWorker);
    return thisWorker;
  }

  default <C, P> AbstractWorker<C, P> and(
      EntityLock lock, BiConsumer<AbstractWorker<C, P>, C> onProcess) {
    AbstractWorker<C, P> thisWorker = new ChainAbstractWorker(lock, onProcess);
    toDiagnostic(thisWorker);
    return thisWorker;
  }

  default <C, P> void toDiagnostic(AbstractWorker<C, P> thisWorker) {
    diagnosticService().toDiagnostic(thisWorker);
  }

  class ChainAbstractWorker<C, P> extends AbstractWorker<C, P> {

    private BiConsumer<AbstractWorker<C, P>, C> worker;

    /** GGlib needs that to instantiate mocks/spies. */
    ChainAbstractWorker() {}

    private ChainAbstractWorker(String entityGUID, BiConsumer<AbstractWorker<C, P>, C> onProcess) {
      super(entityGUID);
      this.worker = onProcess;
    }

    private ChainAbstractWorker(
        EntityLock thisContext, BiConsumer<AbstractWorker<C, P>, C> onProcess) {
      super(thisContext);
      this.worker = onProcess;
    }

    @Override
    protected void onProcess(C model) {
      worker.accept(this, model);
    }
  }
}
