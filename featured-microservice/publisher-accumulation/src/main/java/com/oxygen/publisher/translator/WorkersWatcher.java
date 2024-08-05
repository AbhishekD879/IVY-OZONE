package com.oxygen.publisher.translator;

import java.lang.ref.WeakReference;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Supplier;
import lombok.Getter;

/** Created by Aliaksei Yarotski on 1/10/18. */
@Getter
public final class WorkersWatcher {

  private String chainId;
  private final long created;
  private Supplier<String> diagnostic;
  private final List<WeakReference<AbstractWorker>> followers;

  public WorkersWatcher(String chainId) {
    this.chainId = chainId;
    this.created = System.currentTimeMillis();
    this.followers = new CopyOnWriteArrayList<>();
  }

  public void add(AbstractWorker<?, ?> abstractWorker) {
    followers.add(new WeakReference(abstractWorker));
  }

  public static WorkersWatcher createWatcher(String chainId) {
    WorkersWatcher result = new WorkersWatcher(chainId);
    result.diagnostic =
        () -> {
          StringBuffer errors = new StringBuffer();
          result
              .getFollowers()
              .forEach(
                  weak -> {
                    try {
                      final AbstractWorker<?, ?> thisWorker = weak.get();
                      if (thisWorker != null && thisWorker.isWorking()) {
                        errors.append(thisWorker.getChainId()).append(" >>chain>> ");
                        thisWorker.finalizeWork();
                      }
                    } catch (NullPointerException e) {
                      errors.append("The workers' thread has been interrupted.");
                    } catch (Exception e) {
                      errors
                          .append("The workers' thread has been interrupted by exception: ")
                          .append(e.getMessage());
                    }
                  });
          return errors.toString();
        };
    return result;
  }

  public boolean isAlive() {
    if (followers.size() == 0) {
      return false;
    }
    AbstractWorker rootWorker = followers.get(0).get();
    if (rootWorker == null) {
      return false;
    }
    if (followers.size() == 1 && !this.chainId.equals(rootWorker.getChainId())) {
      return false;
    }
    return rootWorker.isWorking();
  }
}
