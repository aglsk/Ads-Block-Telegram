function doGet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("PalavrasSuspeitas");
  var palavras = sheet.getRange(2, 1, sheet.getLastRow() - 1, 1).getValues(); // Pega as palavras a partir da linha 2
  
  var palavrasSuspeitas = palavras.map(function(row) {
    return row[0];  // Pegando cada palavra da primeira coluna
  });

  // Retorna as palavras como JSON
  var jsonResponse = {
    "PALAVRAS_SUSPEITAS": palavrasSuspeitas
  };
  
  return ContentService.createTextOutput(JSON.stringify(jsonResponse)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    // Lê os dados enviados via POST
    var dados = JSON.parse(e.postData.contents); // Aqui, obtemos os dados do POST em formato JSON

    // Acessa a lista de palavras suspeitas
    var palavrasSuspeitas = dados.palavras;

    // Acessa a planilha e define a aba correta
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PalavrasSuspeitas');
    
    // Adiciona cada palavra na planilha
    palavrasSuspeitas.forEach(function(palavra) {
      sheet.appendRow([palavra]);
    });

    // Retorna uma resposta de sucesso
    return ContentService.createTextOutput("Palavras atualizadas com sucesso.");

  } catch (error) {
    // Se houver um erro, retornamos a mensagem de erro
    return ContentService.createTextOutput("Erro: " + error.message);
  }
}
