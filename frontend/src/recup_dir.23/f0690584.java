recommend that you report the issue to the extension authors.</property>
                        <property name="justify">center</property>
                        <property name="wrap">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkFrame">
                        <property name="margin-top">12</property>
                        <child>
                          <object class="GtkBox">
                            <property name="hexpand">True</property>
                            <property name="orientation">vertical</property>
                            <child>
                              <object class="GtkBox" id="expander">
                                <property name="spacing">6</property>
                                <style>
                                  <class name="expander"/>
                                </style>
                                <child>
                                  <object class="GtkImage" id="expanderArrow">
                                    <property name="icon-name">pan-end-symbolic</property>
                                  </object>
                                </child>
                                <child>
                                  <object class="GtkLabel">
                                    <property name="label" translatable="yes">Technical Details</property>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child>
                              <object class="GtkRevealer" id="revealer">
                                <child>
                                  <object class="GtkBox">
                                    <property name="orientation">vertical</property>
                                    <child>
                                      <object class="GtkTextView" id="errorView">
                                        <property name="monospace">True</property>
                                        <property name="editable">False</property>
                                        <property name="wrap-mode">word</property>
                                        <property name="left-margin">12</property>
                                        <property name="right-margin">12</property>
                                        <property name="top-margin">12</property>
                                        <property name="bottom-margin">12</property>
                                      </object>
                                    </child>
                                    <child>
                                      <object class="GtkBox">
                                        <style>
                                          <class name="expander-toolbar"/>
                                        </style>
                                        <child>
                                          <object class="GtkButton">
                                            <property name="receives-default">True</property>
                                            <property name="action-name">win.copy-error</property>
                                            <property name="has-frame">False</property>
                                            <property name="icon-name">edit-copy-symbolic</property>
                                          </object>
                                        </child>
                                        <child>
                                          <object class="GtkButton" id="homeButton">
                                            <property name="visible"
                                                      bind-source="homeButton"
                                                      bind-property="sensitive"
                                                      bind-flags="sync-create"/>
                                            <property name="hexpand">True</property>
                                            <property name="halign">end</property>
                                            <property name="label" translatable="yes">Homepage</property>
                                            <property name="tooltip-text" translatable="yes">Visit extension homepage</property>
                                            <property name="receives-default">True</property>
                                            <property name="has-frame">False</property>
                                            <property name="action-name">win.show-url</property>
                                          </object>
                                        </child>
                                      </object>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </template>
</interface>
