import clean from './clean';import ThirdPartyLibsLoader from './3rd-party';

export default {
  run(environmentConfig) {
    clean.run();
    ThirdPartyLibsLoader.run();}
};
