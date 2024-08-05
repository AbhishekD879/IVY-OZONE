package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.storage.Storage;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.redisson.api.RLock;

@RunWith(MockitoJUnitRunner.class)
public class LockServiceAsyncTest {

  @Mock Storage storage;

  @Mock DataCallback dataCallback;

  @Mock RLock lock;

  private LockService lockService;

  @Before
  public void setUp() throws InterruptedException {
    Mockito.when(storage.getLock(Mockito.anyString())).thenReturn(lock);
    setLockAvailable(true);

    lockService = new LockService(storage);
  }

  private void setLockAvailable(boolean available) throws InterruptedException {
    Mockito.when(lock.tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any()))
        .thenReturn(available);
  }

  private void verifyLockedUnlocked() throws InterruptedException {
    Mockito.verify(lock, Mockito.timeout(100))
        .tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.timeout(100)).forceUnlock();
  }

  private void verifyOnlyLocked() throws InterruptedException {
    Mockito.verify(lock, Mockito.timeout(100))
        .tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.after(100).never()).forceUnlock();
    Mockito.verify(lock, Mockito.after(100).never()).unlock();
  }

  @Test
  public void testDontWrap() throws InterruptedException {
    lockService.tryLockWithWrapper("", 1, wrapper -> {});
    verifyLockedUnlocked();
  }

  @Test
  public void testThrowException() throws InterruptedException {
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          throw new RuntimeException();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testWrapAndThrowException() throws InterruptedException {
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          wrapper.wrap(dataCallback);
          throw new RuntimeException();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testWrapAndDontCallCallback() throws InterruptedException {
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          wrapper.wrap(dataCallback);
        });
    verifyOnlyLocked();
  }

  @Test
  public void testWrapCallSuccess() throws InterruptedException {
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          DataCallback wrap = wrapper.wrap(dataCallback);
          new Thread(
                  () -> {
                    wrap.onResponse(null);
                  })
              .start();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testWrapCallError() throws InterruptedException {
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          DataCallback wrap = wrapper.wrap(dataCallback);
          new Thread(
                  () -> {
                    wrap.onError(new RuntimeException());
                  })
              .start();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testWrapCallErrorWithException() throws InterruptedException {
    Mockito.doThrow(new RuntimeException()).when(dataCallback).onError(Mockito.any());

    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          DataCallback wrap = wrapper.wrap(dataCallback);
          new Thread(
                  () -> {
                    wrap.onError(new RuntimeException());
                  })
              .start();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testWrapCallSucessWithException() throws InterruptedException {
    Mockito.doThrow(new RuntimeException()).when(dataCallback).onResponse(Mockito.any());

    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          DataCallback wrap = wrapper.wrap(dataCallback);
          new Thread(
                  () -> {
                    wrap.onResponse(null);
                  })
              .start();
        });
    verifyLockedUnlocked();
  }

  @Test
  public void testIsLocked() throws InterruptedException {
    setLockAvailable(false);
    Runnable runnable = Mockito.mock(Runnable.class);
    lockService.tryLockWithWrapper(
        "",
        1,
        wrapper -> {
          runnable.run();
        });
    verifyOnlyLocked();
    Mockito.verify(runnable, Mockito.never()).run();
  }
}
