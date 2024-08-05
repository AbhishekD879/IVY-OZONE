package com.egalacoral.spark.timeform.storage;

import java.util.List;
import java.util.Map;
import java.util.Set;
import org.redisson.api.RLock;

public interface Storage {
  /**
   * Returns the distributed set instance with the specified name.
   *
   * @param name name of the distributed set
   * @return distributed set instance with the specified name
   */
  <E> Set<E> getSet(String name);

  /**
   * Returns the distributed list instance with the specified name. Index based operations on the
   * list are not supported.
   *
   * @param name name of the distributed list
   * @return distributed list instance with the specified name
   */
  <E> List<E> getList(String name);

  /**
   * Returns the distributed map instance with the specified name.
   *
   * @param name name of the distributed map
   * @return distributed map instance with the specified name
   */
  <K, V> Map<K, V> getMap(String name);

  /**
   * Returns the distributed lock instance for the specified key object. The specified object is
   * considered to be the key for this lock. So keys are considered equals cluster-wide as long as
   * they are serialized to the same byte array such as String, long, Integer.
   *
   * <p>Locks are fail-safe. If a member holds a lock and some of the members go down, the cluster
   * will keep your locks safe and available. Moreover, when a member leaves the cluster, all the
   * locks acquired by this dead member will be removed so that these locks can be available for
   * live members immediately.
   *
   * <pre>
   * Lock lock = hazelcastInstance.getLock("PROCESS_LOCK");
   * lock.lock();
   * try {
   *   // process
   * } finally {
   *   lock.unlock();
   * }
   * </pre>
   *
   * @param key key of the lock instance
   * @return distributed lock instance for the specified key.
   */
  RLock getLock(String key);
}
