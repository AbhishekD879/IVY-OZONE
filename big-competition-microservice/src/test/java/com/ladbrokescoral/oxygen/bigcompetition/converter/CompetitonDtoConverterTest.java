package com.ladbrokescoral.oxygen.bigcompetition.converter;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import java.util.Arrays;
import java.util.Collection;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitonDtoConverterTest {

  @Mock private CompetitionTabDtoConverter competitionTabDtoConverter;

  @InjectMocks private CompetitionDtoConverter converter;

  @Test
  public void testCompetitionMap() {

    CompetitionTabDto competitionTabDto = new CompetitionTabDto();
    competitionTabDto.setId("1");
    competitionTabDto.setName("worldCup");
    competitionTabDto.setTitle("worldcup");

    Competition competition = new Competition();
    competition.setId("1122");
    competition.setName("FIFA");
    competition.setPath("/FIFA");

    Mockito.when(competitionTabDtoConverter.convert(Mockito.any(Collection.class)))
        .thenReturn(Arrays.asList(competitionTabDto));

    CompetitionDto competitionDto = converter.map(competition);
    Assert.assertNotNull(competitionDto);
  }
}
