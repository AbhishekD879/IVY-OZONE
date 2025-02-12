##ITCSS, by default, has seven layers.

01. ####Settings

  If you are using a preprocessor, start here. This holds any global settings for your project. I'd like to stress the word global – this layer should only house settings that need to be accessed from anywhere. Settings like `$heading-size-1` should be defined in the Headings partial. This ensures this layer stays nice and slim, and means that most settings can be found alongside the code that uses them, making finding things far simpler

  Examples of global settings might be things like the base font size, colour palettes, config (for example, `$environment: dev;`) and so on.

02. ####Tools

  The next layer houses your globally available tooling – namely mixins and functions. Any mixin or function that does not need accessing globally should belong in the partial to which it relates. The Tools layer comes after the Settings layer because a mixin may require one of the global settings as a default parameter. Examples of global tools might be gradient mixins, font-sizing mixins and so on.

03. ####Generic

  The Generic layer is the first one that actually produces any CSS. It houses very high-level, far reaching styles. This layer is seldom modified, and is usually the same across any projects you work on. It contains things like Normalize.css, global box-sizing rules, CSS resets and so on. The Generic layer affects a lot of the DOM, hence it being nice and wide in the Triangle model, and occurring very early on.

04. ####Elements

  These are bare, unclassed HTML elements. What does an h1 look like without a class on it? What does an a look like without a class on it? The Elements layer binds onto bare HTML element (or 'type') selectors only. It is slightly more explicit than the previous layer in that we are now saying 'make every h1 this big', or 'make every a be a certain colour'. It is still a very low-specificity layer, but affects slightly less of the DOM, and is slightly more opinionated, hence its location in the Triangle.

  The Elements layer is typically the last one in which we'd find bare, element-based selectors, and is very rarely added to or changed after initial setup. Once we have defined element-level styles, all additions and deviations should be implemented using classes.

05. ####Objects

  Users of OOCSS will be familiar with the concept of objects. This is the first layer in which we find class-based selectors. These are concerned with styling non-cosmetic design patterns, or 'objects'. Objects can range from something as simple as a .wrapper element, to layout systems, through to things like the OOCSS poster child – the Media Object. This layer affects less of the DOM than the last layer, has a higher specificity, and is slightly more explicit in that we are now targeting sections of the DOM with classes.

06. ####Components

  The Components layer is where we begin to style recognisable pieces of UI. We're still binding onto classes here, so our specificity hasn't yet increased. However, this layer is more explicit than the last one in that we are now styling explicit, designed pieces of the DOM.

  We shouldn't find any selectors with a lower specificity than one class in this layer. This is where the majority of your work will happen after initial project set-up. Adding new components and features usually makes up the vast majority of development.

07. ####Trumps

  This layer beats – or 'trumps' – all other layers, and has the power to override anything at all that has gone before it. It is inelegant and heavy-handed, and contains utility and helper classes, hacks and overrides.

  A lot of the declarations in this layer will carry !important (e.g. .text-center { text-align: centre !important; }). This is the highest specificity layer – it includes the most explicit types of rule, with the most narrow focus. This layer forms the point of the Triangle.
