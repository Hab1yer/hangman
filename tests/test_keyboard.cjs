const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');

// Exercise the actual application's event handler with a focused button.
const elements = {};
for (const id of ['new','keyboard','pattern','remaining','wrong','figure','status','difficulty']) {
  elements[id] = {children: [], style: {}, value: 'easy', append(b) {this.children.push(b);}, click() {}};
}
let keydown;
const context = vm.createContext({
  document: {
    getElementById: id => elements[id],
    createElement: () => ({}),
    addEventListener: (name, fn) => {keydown = fn;},
  },
});
vm.runInContext(readFileSync('static/app.js', 'utf8'), context);
vm.runInContext('var recorded = []; guess = letter => recorded.push(letter);', context);
let prevented = false;
keydown({key:'E', target:{tagName:'BUTTON'}, preventDefault() {prevented = true;}});
assert.equal(vm.runInContext('recorded.join()', context), 'e');
assert.ok(prevented);
for (const tagName of ['INPUT','TEXTAREA','SELECT']) {
  keydown({key:'a', target:{tagName}});
}
keydown({key:'a', ctrlKey:true, target:{tagName:'BUTTON'}});
keydown({key:'a', repeat:true, target:{tagName:'BUTTON'}});
assert.equal(vm.runInContext('recorded.join()', context), 'e');
console.log('PASS: letter keys work with button focus; input fields, shortcuts and repeats are ignored.');
