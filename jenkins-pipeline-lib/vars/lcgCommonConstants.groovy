def call(String key = "") {

    def constants = [:]

    constants << lcgCommonConstantsGeneral()
    constants << lcgCommonConstantsServices()
    constants << lcgCommonConstantsEnvsDev0Coral()
    constants << lcgCommonConstantsEnvsDev0Ladbrokes()
    constants << lcgCommonConstantsEnvsDevVanilla()
    constants << lcgCommonConstantsEnvsAkamaiCoral()
    constants << lcgCommonConstantsEnvsAwsCoral()
    constants << lcgCommonConstantsEnvsAwsCoralCloudFront()
    constants << lcgCommonConstantsEnvsAkamaiLadbrokes()
    constants << lcgCommonConstantsEnvsAwsLadbrokes()
    constants << lcgCommonConstantsEnvsCloudFlareCoral()
    constants << lcgCommonConstantsEnvsCloudFlareLadbrokes()

    if (key.length() > 0) {
        return constants[key]
    }
    else {
        return constants
    }

}
