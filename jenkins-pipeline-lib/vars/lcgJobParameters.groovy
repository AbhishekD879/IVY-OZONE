/**
 * Change String param value during build
 *
 * @param paramName         new or existing param name
 * @param paramValue        param value
 * @param paramDescription  param description
 * @param paramTrim         param trim
 * @return nothing
 */
 def addString(String paramName, String paramValue, String paramDescription, Boolean paramTrim) {
    addString($build().getParent(), paramName, paramValue, paramDescription, paramTrim)
}

/**
 * Change String param value to the given job
 *
 * @param job               job object
 * @param paramName         new or existing param name
 * @param paramValue        param value
 * @param paramDescription  param description
 * @param paramTrim         param trim
 * @return nothing
 */
def addString(Job job, String paramName, String paramValue, String paramDescription, Boolean paramTrim) {
    ParametersDefinitionProperty paramsJobProperty = job.getProperty(ParametersDefinitionProperty.class);
    List<ParameterDefinition> newJobParams = new ArrayList<>();

    if (paramsJobProperty) {
        List<ParameterDefinition> oldJobParams = paramsJobProperty.getParameterDefinitions();

        for (ParameterDefinition p: oldJobParams) {
            if (!p.getName().equals(paramName)) {
                newJobParams.add(0,p);
            }
        }

        job.removeProperty(paramsJobProperty)

    }

    StringParameterDefinition newStringParam = new StringParameterDefinition(paramName, paramValue, paramDescription, paramTrim)
    newJobParams.add(newStringParam)
    ParametersDefinitionProperty newParamsJobProperty = new ParametersDefinitionProperty(newJobParams);
    job.addProperty(newParamsJobProperty);
}

/**
 * Add a new option to choice parameter for the current job
 *
 * @param paramName parameter name
 * @param optionValue option value
 * @return nothing
 */
def addChoice(String paramName, String optionValue) {
    addChoice($build().getParent(), paramName, optionValue)
}

/**
 * Add a new option to choice parameter to the given job
 * @param job job object
 * @param paramName parameter name
 * @param optionValue option value
 * @return
 */
def addChoice(Job job, String paramName, String optionValue) {
    ParametersDefinitionProperty paramsJobProperty = job.getProperty(ParametersDefinitionProperty.class);
    ChoiceParameterDefinition oldChoiceParam = (ChoiceParameterDefinition)paramsJobProperty.getParameterDefinition(paramName);
    List<ParameterDefinition> oldJobParams = paramsJobProperty.getParameterDefinitions();
    List<ParameterDefinition> newJobParams = new ArrayList<>();

    for (ParameterDefinition p: oldJobParams) {
        if (!p.getName().equals(paramName)) {
            newJobParams.add(0,p);
        }
    }

    List<String> choices = new ArrayList(oldChoiceParam.getChoices());

    choices.add(optionValue);
    ChoiceParameterDefinition newChoiceParam = new ChoiceParameterDefinition(paramName, choices, oldChoiceParam.getDefaultParameterValue().getValue(), oldChoiceParam.getDescription());
    newJobParams.add(newChoiceParam);

    ParametersDefinitionProperty newParamsJobProperty = new ParametersDefinitionProperty(newJobParams);
    job.removeProperty(paramsJobProperty);
    job.addProperty(newParamsJobProperty);
}
