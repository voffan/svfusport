var Competition = Backbone.Model;
var CompetitionCollection = Backbone.Collection.extend({});
var competition = new CompetitionCollection(JSON.parse('{{json_collection}}'));
//competition.fetch();
//alert(competition);

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
  //alert(this.model.get('competition_id'));
  this.$el.html('<td>'+'<input type="checkbox" class="one" data-id="d1" id="checkbox' + this.model.get('id') + '">'+'</td><td>' + this.model.get('id') + '</td><td><a href="' + this.model.get('url') + '">' + this.model.get('sport') + '</a>' + '</td><td>' + this.model.get('date') + '</td><td>' + this.model.get('place') + '</td>');
  //this.$el.html('<td  style="background: white;">' + this.model.get('id') + '</td><td style="background: white;"><a href="/CM/competitionedit/' + this.model.get('competition_id') + '">' + this.model.get('sport') + '</a>' + '</td><td style="background: white;">' + this.model.get('date') + '</td><td style="background: white;">' + this.model.get('place') + '</td>');
      return this;
}
});

new CollectionView;
