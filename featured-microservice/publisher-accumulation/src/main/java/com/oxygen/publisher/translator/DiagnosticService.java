package com.oxygen.publisher.translator;

import com.newrelic.api.agent.Trace;
import java.util.ArrayList;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Consumer;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

/** Created by Aliaksei Yarotski on 1/5/18. */
@Slf4j
public class DiagnosticService extends Thread {

  private final long waitForDiagnosticsTime;

  @Getter private final Map<String, WorkersWatcher> watchers;
  @Getter @Setter private boolean keepRunning;

  private Consumer<String> onProblemListener;

  public DiagnosticService(long waitForDiagnosticsTime) {
    this.waitForDiagnosticsTime = waitForDiagnosticsTime;
    this.watchers = new ConcurrentHashMap<>();
    this.keepRunning = true;
  }

  public WorkersWatcher toDiagnostic(AbstractWorker worker) {
    WorkersWatcher watcher = null;
    String chainId = null;
    try {
      chainId = worker.getChainId();
      watcher = watchers.get(chainId);
      if (watcher == null) {
        watcher = WorkersWatcher.createWatcher(chainId);
        watcher.add(worker);
        watchers.put(chainId, watcher);
      } else {
        watcher.add(worker);
      }
    } catch (Exception e) {
      log.error("[ DS ] Worker watcher not created. Chain ID {}", chainId, e);
    }
    return watcher;
  }

  @Override
  public void run() {
    try {
      while (keepRunning) {
        sleep(waitForDiagnosticsTime);
        final long deadline = System.currentTimeMillis() - waitForDiagnosticsTime;
        final ArrayList<String> toBeDeleted = new ArrayList<>();
        watchers
            .values()
            .forEach(
                watch -> {
                  if (!watch.isAlive()) {
                    toBeDeleted.add(watch.getChainId());
                  } else if (watch.getCreated() < deadline) {
                    final String warnings = watch.getDiagnostic().get();
                    if (StringUtils.isNoneBlank(warnings)) {
                      processWarnings(
                          "[ DS ]"
                              + watch.getChainId()
                              + " process still working and have a problems: "
                              + warnings);
                    }
                  }
                });
        toBeDeleted.forEach(id -> watchers.remove(id));
        log.trace("[ DS ] waiting for GC {}", watchers.size());
      }
    } catch (InterruptedException e) {
      log.error(e.getMessage(), e);
      Thread.currentThread().interrupt();
    }
  }

  @Trace(metricName = "sportFDiagnosticsProblems", dispatcher = true)
  public void processWarnings(String warnings) {
    if (onProblemListener != null) {
      onProblemListener.accept(warnings);
    }
    log.trace("[ DS ] Diagnostics problems detected: {}", warnings);
  }

  public void setDiagnosticListener(Consumer<String> listener) {
    this.onProblemListener = listener;
  }
}
