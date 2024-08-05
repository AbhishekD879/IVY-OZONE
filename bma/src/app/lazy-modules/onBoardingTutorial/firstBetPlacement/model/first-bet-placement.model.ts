export interface IFirstBetDetails {
    id: string,
    createdBy: string,
    createdByUserName: string,
    updatedBy: string,
    updatedByUserName: string,
    createdAt: string,
    updatedAt: string,
    brand: string,
    months: number,
    isEnable: true,
    moduleName: string,
    moduleDiscription: string,
    displayFrom: string,
    displayTo: string,
    expiryDateEnabled: boolean,
    imageUrl: string,
    fileName: string,
    heightMedium: number,
    widthMedium: number,
    button: {
        title: string,
        description: string,
        leftButtonDesc: string,
        rightButtonDesc: string  },
    homePage: {
        title: string,
        description: string,
        button: string  },
    pickYourBet: {
        title: string,
        description: string  },
    addSelection: {
        title: string,
        description: string  },
    betSlip: {
        boost: {
        title: string,
        description: string    },
        defaultContent: {
        title: string,
        description: string    }
    },
    placeYourBet: {
        boost: {
            title: string,
            description: string    
        },
        defaultContent: {
            title: string,
            description: string    
        }
    },
    betPlaced: {
        winAlert: {
            title: string,
            description: string
        },
        defaultContent: {
            title: string,
            description: string    
        },
        buttonDesc: string
    },
    myBets: {
        cashOut: {
        title: string,
        description: string    },
        defaultContent: {
        title: string,
        description: string    },
        buttonDesc: string  },
    betDetails: {
        cashOut: {
        title: string,
        description: string    },
        defaultContent: {
        title: string,
        description: string    }
    }
  }