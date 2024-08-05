package com.ladbrokescoral.cashout.service.masterslave;

import static com.ladbrokescoral.cashout.repository.LockRepository.REDIS_SAVER_LOCK;

import com.ladbrokescoral.cashout.model.RedisSaverLock;
import com.ladbrokescoral.cashout.repository.ReactiveLockRepository;
import com.ladbrokescoral.cashout.util.Message;
import java.time.Instant;
import java.util.UUID;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class MasterSlaveService implements MasterSlave {

  private final int changeMasterAfter;
  private final ReactiveLockRepository<RedisSaverLock> lockRepository;
  private final String uuid = UUID.randomUUID().toString();
  private volatile boolean isMaster = false;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message messages;

  public MasterSlaveService(
      @Value("${distributed.master.change}") int changeMasterAfter,
      ReactiveLockRepository<RedisSaverLock> lockRepository) {
    this.changeMasterAfter = changeMasterAfter;
    this.lockRepository = lockRepository;
  }

  @Override
  public boolean isMaster() {
    return isMaster;
  }

  @Scheduled(fixedRateString = "${distributed.master.check}")
  public void process() {
    try {
      lockRepository
          .getLock(REDIS_SAVER_LOCK)
          .switchIfEmpty(Mono.just(createNewLock()))
          .map(
              lock -> {
                if (!shouldBeMaster(lock)) {
                  isMaster = false;
                  ASYNC_LOGGER.debug("Instance IS NOT a master");
                  return Mono.empty();
                } else {
                  isMaster = true;
                  ASYNC_LOGGER.debug("Instance IS a master");
                  lockRepository.saveLock(REDIS_SAVER_LOCK, createNewLock()).subscribe();
                  return lock;
                }
              })
          .subscribe();
    } catch (Exception e) {
      ASYNC_LOGGER.error("Issue in master slave operations - ", e);
    }
  }

  private RedisSaverLock createNewLock() {
    return RedisSaverLock.builder().timestamp(Instant.now().toEpochMilli()).uuid(uuid).build();
  }

  private boolean shouldBeMaster(RedisSaverLock lock) {
    messages = new Message();
    messages.setMessage(lock.toString());
    boolean result = uuid.equals(lock.getUuid()) || isLockExpired(lock);
    ASYNC_LOGGER.trace(
        "Should be a master - {}, excecutor instance uuid - {}, lock - {}", result, uuid, messages);
    return result;
  }

  private boolean isLockExpired(RedisSaverLock lock) {
    boolean result = Instant.now().toEpochMilli() > lock.getTimestamp() + changeMasterAfter;
    if (result) {
      ASYNC_LOGGER.info(
          "Lock expired - {}, excecutor instance uuid - {}, lock - {}", result, uuid, lock);
    }
    return result;
  }
}
