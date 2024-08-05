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
public class LockServiceSyncTest {

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
    Mockito.verify(lock, Mockito.timeout(100)).unlock();
  }

  private void verifyOnlyLocked() throws InterruptedException {
    Mockito.verify(lock, Mockito.timeout(100))
        .tryLock(Mockito.anyLong(), Mockito.anyLong(), Mockito.any());
    Mockito.verify(lock, Mockito.after(100).never()).unlock();
    Mockito.verify(lock, Mockito.after(100).never()).forceUnlock();
  }

  @Test
  public void testRunInLock() throws InterruptedException {
    setLockAvailable(true);
    Runnable runnable = Mockito.mock(Runnable.class);
    lockService.doInLockOrSkip(
        "",
        1,
        () -> {
          runnable.run();
        });
    Mockito.verify(runnable).run();
    verifyLockedUnlocked();
  }

  @Test
  public void testSkip() throws InterruptedException {
    setLockAvailable(false);
    Runnable runnable = Mockito.mock(Runnable.class);
    lockService.doInLockOrSkip(
        "",
        1,
        () -> {
          runnable.run();
        });
    Mockito.verify(runnable, Mockito.never()).run();
    verifyOnlyLocked();
  }
}
