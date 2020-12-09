dirty = '<div aria-labelledby="msg--title" role="dialog" class="msg"><button class="modal-close" aria-label="close" type="button"><i class="icon-close"></i>some button</button></div>';

const createDOMPurify = require('./purify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const clean = DOMPurify.sanitize(dirty);
console.log(clean);
