#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'api.laurabeth@gmail.com (Laura Beth Lincoln)'


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.spreadsheet.service
import getopt
import string
import sys


class SimpleCRUD:

  def __init__( self, email, password ):
    self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    self.gd_client.email = email
    self.gd_client.password = password
    self.gd_client.source = 'Spreadsheets GData Sample'
    self.gd_client.ProgrammaticLogin()
    self.curr_key = ''
    self.curr_wksht_id = ''
    self.list_feed = None
    self._SelectExcel()

  def ReadCellContent(self, cell):
    self.gd_client.GetCellsFeed( self.curr_key, self.curr_wksht_id , cell)
     
  def _PromptForSpreadsheet( self ):
    # Get the list of spreadsheets
    feed = self.gd_client.GetSpreadsheetsFeed()
    self._PrintFeed( feed )
    input = raw_input( '\nSelection: ' )
    id_parts = feed.entry[string.atoi( input )].id.text.split( '/' )
    self.curr_key = id_parts[len( id_parts ) - 1]

  def _PromptForWorksheet( self ):
    # Get the list of worksheets
    feed = self.gd_client.GetWorksheetsFeed( self.curr_key )
    self._PrintFeed( feed )
    input = raw_input( '\nSelection: ' )
    id_parts = feed.entry[string.atoi( input )].id.text.split( '/' )
    self.curr_wksht_id = id_parts[len( id_parts ) - 1]

  def _SelectExcel(self):
    feed = self.gd_client.GetSpreadsheetsFeed()
    id_parts = feed.entry[string.atoi( "1" )].id.text.split( '/' )
    self.curr_key = id_parts[len( id_parts ) - 1]
    feed = self.gd_client.GetWorksheetsFeed( self.curr_key )
    id_parts = feed.entry[string.atoi( "1" )].id.text.split( '/' )
    self.curr_wksht_id = id_parts[len( id_parts ) - 1]
    
    
  def get(self, row, col):
    query = gdata.spreadsheet.service.CellQuery()
    query['min-col'] = query['max-col'] = str(col)
    query['min-row'] = query['max-row'] = str(row)
    cells = self.gd_client.GetCellsFeed(self.curr_key, self.curr_wksht_id, query=query)
    return cells.entry[0].content.text
  
  def update(self, row, col, val):
    entry = self.gd_client.UpdateCell( row , col, inputValue = val,
        key = self.curr_key, wksht_id = self.curr_wksht_id )
    if isinstance( entry, gdata.spreadsheet.SpreadsheetsCell ):
      print 'Updated!'

  def _PromptForCellsAction( self ):
    print ( 'dump\n'
           'update {row} {col} {input_value}\n'
           '\n' )
    input = raw_input( 'Command: ' )
    command = input.split( ' ', 1 )
    if command[0] == 'dump':
      self._CellsGetAction()
    elif command[0] == 'update':
      parsed = command[1].split( ' ', 2 )
      if len( parsed ) == 3:
        self._CellsUpdateAction( parsed[0], parsed[1], parsed[2] )
      else:
        self._CellsUpdateAction( parsed[0], parsed[1], '' )
    else:
      self._InvalidCommandError( input )

  def _PromptForListAction( self ):
    print ( 'dump\n'
           'insert {row_data} (example: insert label=content)\n'
           'update {row_index} {row_data}\n'
           'delete {row_index}\n'
           'Note: No uppercase letters in column names!\n'
           '\n' )
    input = raw_input( 'Command: ' )
    command = input.split( ' ' , 1 )
    if command[0] == 'dump':
      self._ListGetAction()
    elif command[0] == 'insert':
      self._ListInsertAction( command[1] )
    elif command[0] == 'update':
      parsed = command[1].split( ' ', 1 )
      self._ListUpdateAction( parsed[0], parsed[1] )
    elif command[0] == 'delete':
      self._ListDeleteAction( command[1] )
    else:
      self._InvalidCommandError( input )

  def _CellsGetAction( self ):
    # Get the feed of cells
    feed = self.gd_client.GetCellsFeed( self.curr_key, self.curr_wksht_id )
    self._PrintFeed( feed )

  def _CellsUpdateAction( self, row, col, inputValue ):
    entry = self.gd_client.UpdateCell( row = row, col = col, inputValue = inputValue,
        key = self.curr_key, wksht_id = self.curr_wksht_id )
    if isinstance( entry, gdata.spreadsheet.SpreadsheetsCell ):
      print 'Updated!'

  def _ListGetAction( self ):
    # Get the list feed
    self.list_feed = self.gd_client.GetListFeed( self.curr_key, self.curr_wksht_id )
    self._PrintFeed( self.list_feed )

  def _ListInsertAction( self, row_data ):
    entry = self.gd_client.InsertRow( self._StringToDictionary( row_data ),
        self.curr_key, self.curr_wksht_id )
    if isinstance( entry, gdata.spreadsheet.SpreadsheetsList ):
      print 'Inserted!'

  def _ListUpdateAction( self, index, row_data ):
    self.list_feed = self.gd_client.GetListFeed( self.curr_key, self.curr_wksht_id )
    entry = self.gd_client.UpdateRow( 
        self.list_feed.entry[string.atoi( index )],
        self._StringToDictionary( row_data ) )
    if isinstance( entry, gdata.spreadsheet.SpreadsheetsList ):
      print 'Updated!'

  def _ListDeleteAction( self, index ):
    self.list_feed = self.gd_client.GetListFeed( self.curr_key, self.curr_wksht_id )
    self.gd_client.DeleteRow( self.list_feed.entry[string.atoi( index )] )
    print 'Deleted!'

  def _StringToDictionary( self, row_data ):
    dict = {}
    for param in row_data.split():
      temp = param.split( '=' )
      dict[temp[0]] = temp[1]
    return dict

  def _PrintFeed( self, feed ):
    for i, entry in enumerate( feed.entry ):
      if isinstance( feed, gdata.spreadsheet.SpreadsheetsCellsFeed ):
        print '%s %s\n' % ( entry.title.text, entry.content.text )
      elif isinstance( feed, gdata.spreadsheet.SpreadsheetsListFeed ):
        print '%s %s %s' % ( i, entry.title.text, entry.content.text )
        # Print this row's value for each column (the custom dictionary is
        # built using the gsx: elements in the entry.)
        print 'Contents:'
        for key in entry.custom:
          print '  %s: %s' % ( key, entry.custom[key].text )
        print '\n',
      else:
        print '%s %s\n' % ( i, entry.title.text )

  def _InvalidCommandError( self, input ):
    print 'Invalid input: %s\n' % ( input )

  def updateexcel(self, dir):
    pass
  
    
      

def main():
  sample = SimpleCRUD("username", "password")
  #sample.Run()


if __name__ == '__main__':
  main()
