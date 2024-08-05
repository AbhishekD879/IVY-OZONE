
package com.ladbrokescoral.oxygen.questionengine.controller.api.v1;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.service.UserAnswerService;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.web.util.UriComponentsBuilder;

import static org.mockito.Mockito.when;


@AutoConfigureMockMvc(addFilters = false)
@ActiveProfiles("UNIT")
@RunWith(SpringRunner.class)
public class UserAnswerControllerTest {

    @Mock
    UserAnswerService userAnswerService;

    @InjectMocks
    UserAnswerController userAnswerController;

    @Test
    public void findByIdTest() throws Exception {
        UserAnswerDto userAnswerDto = new UserAnswerDto();
        when(userAnswerService.getById(Mockito.any())).thenReturn(userAnswerDto);
        userAnswerDto = userAnswerController.findById("User123", "test4543");
        Assert.assertNotNull(userAnswerDto);
    }

    @Test
    public void saveTest() throws Exception {
        QuizSubmitDto quizSubmitDto = new QuizSubmitDto();
        quizSubmitDto.setQuizId("12dfs343");
        quizSubmitDto.setUsername("Test123");
        UriComponentsBuilder uriComponentsBuilder = UriComponentsBuilder.newInstance();
        UserAnswerDto userAnswerDto = new UserAnswerDto();
        when(userAnswerService.getById(Mockito.any())).thenReturn(userAnswerDto);
        ResponseEntity<UserAnswerDto> response = userAnswerController.save(quizSubmitDto, uriComponentsBuilder);
        Assert.assertNotNull(response);
    }
}
