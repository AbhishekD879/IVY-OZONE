package com.ladbrokescoral.oxygen.bigcompetition.converter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.factory.ModuleServiceFactory;
import com.ladbrokescoral.oxygen.bigcompetition.service.ModuleService;
import com.ladbrokescoral.oxygen.bigcompetition.util.Utils;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import lombok.AllArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
// @Slf4j
@AllArgsConstructor
public class CompetitionModuleDtoConverter
    implements BaseConverter<CompetitionModule, CompetitionModuleDto> {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private ModuleServiceFactory moduleServiceFactory;

  @Override
  public CompetitionModuleDto map(CompetitionModule module) {
    try {
      ModuleService moduleService = moduleServiceFactory.getModuleService(module.getType());
      return moduleService.process(module);
    } catch (Exception e) {
      ASYNC_LOGGER.error(
          String.format("Error during processing %s module %s", module.getType(), module.getId()),
          e);
      Utils.newRelicLogError(e);
      return null;
    }
  }
}
