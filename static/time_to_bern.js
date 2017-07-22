$(function() {
  var source = $('#table-template').html()
  var template = Handlebars.compile(source)

  function tableize(table_selector, data) {
    var table = $(`${table_selector} tbody`)

    for (row_data of data) {
      var row = template(row_data)
      table.append(row)
    }
  }

  function processData(data) {
    tableize('#from_table', data.from)
    tableize('#to_table', data.to)
    tableize('#late_table', data.late)
  }

  function search() {
    var location = $('#location').val()
    $('table tbody').html('')

    var url = `${window.location}data/${location}`
    $.getJSON(url, processData)
  }

  $('form').submit(function(e) {
    e.preventDefault()
    search()
  })
})
