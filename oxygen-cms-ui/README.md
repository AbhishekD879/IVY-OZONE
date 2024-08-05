cookie secret = 'z)BF~TBeOzX;@_JzwTum2cIF3cq0naK;&5o[bvJ,Eu(y_~KiUL9Hy%9PMpTl$n2S'


function hash(str) {
	// force type
	str = '' + str;
	// get the first half
	str = str.substr(0, Math.round(str.length / 2));
	// hash using sha256
	return crypto
		.createHmac('sha256', keystone.get('cookie secret'))
		.update(str)
		.digest('base64')
		.replace(/\=+$/, '');
}

FltPBLDCMgHsPCWbvh8P9FvVyp1ROKMFxu+sWeQ6jOI // JS
FltPBLDCMgHsPCWbvh8P9FvVyp1ROKMFxu+sWeQ6jOI // JAVA

##Installing

Clone this repository and install all project develop dependency.

- `clone this repo`
- `cd oxygen-cms-ui/`
- `npm install`

## Running the UI App:

```
npm run start
```
App will be running on port 4200 (http://cms-localhost.coral.co.uk:4200 as per your hosts configuration).



