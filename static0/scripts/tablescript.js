var Competition = Backbone.Model;
var CompetitionCollection = Backbone.Collection.extend({});
var competition = new CompetitionCollection(JSON.parse('{{json_collection}}'));

var CollectionView = Backbone.View.extend({

template: $('#template').html(),

initialize: function() {

this.collection = competition;
new RowView({ collection: this.collection });
this.collection.on('add', this.addOne, this);
// this.collection.fetch();
$('.search').on("keyup", function(){
console.log('loh');
});

this.render();
},

events: {
'keyup .search': 'search',
},

// Returns array subset of models that match search.
search: function(e) {

var search = this.$('.search').val().toLowerCase();

this.$('tbody').empty(); // is this creating ghost views?

_.each(this.collection.filter(function(model) {
return _.some(
model.values(),
function(value) {
  return ~value.toLowerCase().indexOf(search);
});
}), $.proxy(this.addOne, this));
},

addOne: function(model) {

// add row
var view = new RowView({ model: model });
this.$('tbody').append(view.render().el);
},

render: function() {

// first render
$('#insert').replaceWith(this.$el.html(this.template));
this.collection.each(this.addOne, this);
}
});

var RowView = Backbone.View.extend({

tagName: 'tr',

events: {
// Some detail view will listen for this.
// App.trigger('person:view', this.model);
},

render: function() {

this.$el.html('<td>' + this.model.get('id') + '<td>' + this.model.get('sport') + '</td><td>' + this.model.get('date') + '</td><td>' + this.model.get('place') + '</td>');
return this;
}
});

new CollectionView;
