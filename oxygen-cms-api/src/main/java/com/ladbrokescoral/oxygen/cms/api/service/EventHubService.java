package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.EventHub;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.exception.DependencyDeleteException;
import com.ladbrokescoral.oxygen.cms.api.repository.EventHubRepository;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.ExecutionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class EventHubService extends SortableService<EventHub> {

  private static final int MINIMUM_INDEX_NUMBER = 1;

  private EventHubRepository eventHubRepository;

  private DeleteEntityService deleteEntityService;

  private int maxEventHubs;

  @Autowired
  public EventHubService(
      EventHubRepository eventHubRepository,
      DeleteEntityService deleteEntityService,
      @Value("${eventhub.max-count}") int maxEventHubs) {
    super(eventHubRepository);
    this.eventHubRepository = eventHubRepository;
    this.maxEventHubs = maxEventHubs;
    this.deleteEntityService = deleteEntityService;
  }

  @Override
  protected boolean isNewElementCreatedFirstInTheList() {
    return false;
  }

  public List<EventHub> findAllByBrandAndDisabled(String brand) {
    return eventHubRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, false);
  }

  @Override
  public EventHub prepareModelBeforeSave(EventHub model) {
    Integer indexNumber = model.getIndexNumber();
    if (indexNumber > maxEventHubs || indexNumber < MINIMUM_INDEX_NUMBER) {
      throw new IllegalArgumentException(
          "Please use index number in range : " + MINIMUM_INDEX_NUMBER + " to " + maxEventHubs);
    }
    if (!model.isNew()) {
      Optional<EventHub> savedModel = eventHubRepository.findById(model.getId());
      savedModel.ifPresent(
          (EventHub eventHub) -> {
            model.setIndexNumber(eventHub.getIndexNumber());
            model.setBrand(eventHub.getBrand());
          });
    }
    return super.prepareModelBeforeSave(model);
  }

  public boolean existByBrandAndIndexNumber(String brand, Integer pageId) {
    return eventHubRepository.findOneByBrandAndIndexNumber(brand, pageId).isPresent();
  }

  @Override
  public void delete(String id) {
    findOne(id)
        .ifPresent(
            (EventHub eventHub) -> {
              try {
                deleteDependencies(eventHub);
              } catch (Exception e) {
                throw new DependencyDeleteException(e);
              }
              super.delete(id);
            });
  }

  private void deleteDependencies(EventHub hub) throws InterruptedException, ExecutionException {
    deleteEntityService.delete(
        hub.getIndexNumber().toString(), hub.getBrand(), PageType.eventhub, null);
  }
}
