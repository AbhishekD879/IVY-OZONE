package com.oxygen.publisher.translator;

import com.oxygen.publisher.api.EntityLock;
import java.util.Objects;
import java.util.function.Supplier;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/** produce Created by Aliaksei Yarotski on 12/28/17. */
@Slf4j
@NoArgsConstructor(access = AccessLevel.PACKAGE)
public abstract class AbstractWorker<C, P> {

  @Getter private EntityLock thisContext;

  @Getter private boolean isWorking;

  protected AbstractWorker(String entityGUID) {
    this(
        new EntityLock() {
          @Override
          public String getEntityGUID() {
            return entityGUID;
          }
        });
  }

  protected AbstractWorker(EntityLock context) {
    this.thisContext = Objects.requireNonNull(context, "Workers Context can not be null.");
    Objects.requireNonNull(context.getEntityGUID(), "Workers Context GUID can not be null.");
    this.isWorking = true;
  }

  protected abstract void onProcess(C model);

  public void start(C model) {
    synchronized (thisContext.getEntityGUID().intern()) {
      onProcess(model);
    }
    log.debug(" Work was done for #{} " + thisContext.getEntityGUID());
    isWorking = false;
  }

  public AbstractWorker accept(P result, Supplier<AbstractWorker> factor) {
    AbstractWorker follower = factor.get();
    follower.thisContext = this.thisContext;
    follower.onProcess(result);
    return this;
  }

  /** The following will be NullPointerException. */
  public void finalizeWork() {
    this.onProcess(null);
  }

  public String getChainId() {
    return thisContext.getEntityGUID();
  }
}
